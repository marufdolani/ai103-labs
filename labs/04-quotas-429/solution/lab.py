"""Lab 04 - Quotas, rate limits and resilient retries."""
import random
import time

import openai as openai_sdk

from labkit import cfg, show
from labkit.clients import aoai, project

PROMPT = "Reply with the single word OK."


def one_call(client, model: str):
    return client.responses.create(model=model, input=PROMPT, reasoning={"effort": "low"}, max_output_tokens=200)


def call_with_backoff(model: str, max_attempts: int = 8) -> tuple[bool, int]:
    """Return (succeeded, attempts). Retries 429s honouring retry-after."""
    client = aoai().with_options(max_retries=0)
    # >>> TODO 3: Retry on openai_sdk.RateLimitError; wait retry-after seconds (or 2**attempt + jitter, max 60)
    for attempt in range(1, max_attempts + 1):
        try:
            one_call(client, model)
            return True, attempt
        except openai_sdk.RateLimitError as err:
            header = err.response.headers.get("retry-after") if err.response is not None else None
            wait = float(header) if header else min(60.0, 2 ** attempt + random.uniform(0, 1))
            show.warn(f"429 on attempt {attempt}; sleeping {wait:.1f}s")
            time.sleep(wait)
    return False, max_attempts
    # <<<


def call_with_spillover(primary: str, secondary: str) -> str:
    """Try the primary deployment once; on 429 use the secondary. Returns the deployment that answered."""
    client = aoai().with_options(max_retries=0)
    # >>> TODO 4: On RateLimitError from the primary, send the same request to the secondary deployment
    try:
        one_call(client, primary)
        return primary
    except openai_sdk.RateLimitError:
        one_call(client, secondary)
        return secondary
    # <<<


def main() -> dict:
    throttled = cfg("THROTTLED_MODEL")

    show.step("1. Deployment capacity")
    # >>> TODO 1: Get the throttled deployment and read sku.name and sku.capacity
    dep = project().deployments.get(throttled)
    sku_name, capacity = dep.sku.name, dep.sku.capacity
    # <<<
    show.kv({"deployment": throttled, "sku": sku_name, "capacity": capacity, "TPM": capacity * 1000})

    show.step("2. Burst without retries")
    # >>> TODO 2: Send 8 quick calls with a max_retries=0 client; count successes, 429s and the last retry-after
    client = aoai().with_options(max_retries=0)
    ok = throttled_count = 0
    retry_after = None
    for _ in range(8):
        try:
            one_call(client, throttled)
            ok += 1
        except openai_sdk.RateLimitError as err:
            throttled_count += 1
            retry_after = err.response.headers.get("retry-after") if err.response is not None else None
    # <<<
    show.kv({"succeeded": ok, "throttled (429)": throttled_count, "retry-after": retry_after})

    show.step("3. Same deployment with backoff (waits for the window to reset)")
    outcomes = [call_with_backoff(throttled) for _ in range(2)]
    show.kv({"succeeded": sum(o[0] for o in outcomes), "attempts": [o[1] for o in outcomes]})

    show.step("4. Spillover to a second deployment")
    answered_by = [call_with_spillover(throttled, cfg("SMALL_MODEL")) for _ in range(4)]
    show.kv({"answered by": answered_by})

    return {
        "sku": sku_name,
        "capacity": capacity,
        "burst_throttled": throttled_count,
        "backoff_successes": sum(o[0] for o in outcomes),
        "spillover_used": answered_by.count(cfg("SMALL_MODEL")),
        "spillover_total": len(answered_by),
    }


if __name__ == "__main__":
    show.result(main())
