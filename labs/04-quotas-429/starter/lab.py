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
    # TODO 3: Retry on openai_sdk.RateLimitError; wait retry-after seconds (or 2**attempt + jitter, max 60)
    raise NotImplementedError("TODO 3: Retry on openai_sdk.RateLimitError; wait retry-after seconds (or 2**attempt + jitter, max 60)  (see README step and solution/ if stuck)")


def call_with_spillover(primary: str, secondary: str) -> str:
    """Try the primary deployment once; on 429 use the secondary. Returns the deployment that answered."""
    client = aoai().with_options(max_retries=0)
    # TODO 4: On RateLimitError from the primary, send the same request to the secondary deployment
    raise NotImplementedError("TODO 4: On RateLimitError from the primary, send the same request to the secondary deployment  (see README step and solution/ if stuck)")


def main() -> dict:
    throttled = cfg("THROTTLED_MODEL")

    show.step("1. Deployment capacity")
    # TODO 1: Get the throttled deployment and read sku.name and sku.capacity
    raise NotImplementedError("TODO 1: Get the throttled deployment and read sku.name and sku.capacity  (see README step and solution/ if stuck)")
    show.kv({"deployment": throttled, "sku": sku_name, "capacity": capacity, "TPM": capacity * 1000})

    show.step("2. Burst without retries")
    # TODO 2: Send 8 quick calls with a max_retries=0 client; count successes, 429s and the last retry-after
    raise NotImplementedError("TODO 2: Send 8 quick calls with a max_retries=0 client; count successes, 429s and the last retry-after  (see README step and solution/ if stuck)")
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
