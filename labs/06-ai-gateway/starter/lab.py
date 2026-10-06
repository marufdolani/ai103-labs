"""Lab 06 - AI gateway: per-app token limits with API Management."""
from openai import OpenAI, RateLimitError

from labkit import cfg, show
from labkit.clients import arm, arm_path

APIM_API_VERSION = "2024-05-01"


def subscription_key(app: str) -> str:
    # TODO 1: POST <APIM_RESOURCE_ID>/subscriptions/<app>/listSecrets via ARM and return primaryKey
    raise NotImplementedError("TODO 1: POST <APIM_RESOURCE_ID>/subscriptions/<app>/listSecrets via ARM and return primaryKey  (see README step and solution/ if stuck)")


def gateway_client(key: str) -> OpenAI:
    # TODO 2: OpenAI client pointing at <gateway>/openai/v1/ that sends the APIM subscription key header
    raise NotImplementedError("TODO 2: OpenAI client pointing at <gateway>/openai/v1/ that sends the APIM subscription key header  (see README step and solution/ if stuck)")


def ask(client: OpenAI) -> dict:
    raw = client.responses.with_raw_response.create(
        model=cfg("SMALL_MODEL"), input="Reply OK", reasoning={"effort": "low"}, max_output_tokens=400)
    return {"status": raw.status_code, "remaining": raw.headers.get("x-remaining-tokens")}


def main() -> dict:
    app_a = gateway_client(subscription_key("app-a"))
    app_b = gateway_client(subscription_key("app-b"))

    show.step(f"Burst as app-a (limit {cfg('APIM_TOKENS_PER_MINUTE', '2000')} tokens/min)")
    # TODO 3: Call 10 times as app-a; count successes and 429s; keep the remaining-token headers
    raise NotImplementedError("TODO 3: Call 10 times as app-a; count successes and 429s; keep the remaining-token headers  (see README step and solution/ if stuck)")
    show.kv({"succeeded": successes, "throttled": throttled, "x-remaining-tokens": remaining})

    show.step("app-b right after app-a was throttled")
    # TODO 4: One call as app-b
    raise NotImplementedError("TODO 4: One call as app-b  (see README step and solution/ if stuck)")
    show.kv(app_b_result)

    return {"a_successes": successes, "a_throttled": throttled, "a_remaining": remaining,
            "b_status": app_b_result["status"]}


if __name__ == "__main__":
    show.result(main())
