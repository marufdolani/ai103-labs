"""Lab 06 - AI gateway: per-app token limits with API Management."""
from openai import OpenAI, RateLimitError

from labkit import cfg, show
from labkit.clients import arm, arm_path

APIM_API_VERSION = "2024-05-01"


def subscription_key(app: str) -> str:
    # >>> TODO 1: POST <APIM_RESOURCE_ID>/subscriptions/<app>/listSecrets via ARM and return primaryKey
    resp = arm().post(arm_path(cfg("APIM_RESOURCE_ID"), f"/subscriptions/{app}/listSecrets", APIM_API_VERSION))
    return resp.json()["primaryKey"]
    # <<<


def gateway_client(key: str) -> OpenAI:
    # >>> TODO 2: OpenAI client pointing at <gateway>/openai/v1/ that sends the APIM subscription key header
    return OpenAI(
        base_url=f"{cfg('APIM_GATEWAY_URL').rstrip('/')}/openai/v1/",
        api_key="not-used-gateway-authenticates-with-managed-identity",
        default_headers={"Ocp-Apim-Subscription-Key": key},
        max_retries=0,
    )
    # <<<


def ask(client: OpenAI) -> dict:
    raw = client.responses.with_raw_response.create(
        model=cfg("SMALL_MODEL"), input="Reply OK", reasoning={"effort": "low"}, max_output_tokens=400)
    return {"status": raw.status_code, "remaining": raw.headers.get("x-remaining-tokens")}


def main() -> dict:
    app_a = gateway_client(subscription_key("app-a"))
    app_b = gateway_client(subscription_key("app-b"))

    show.step(f"Burst as app-a (limit {cfg('APIM_TOKENS_PER_MINUTE', '2000')} tokens/min)")
    # >>> TODO 3: Call 10 times as app-a; count successes and 429s; keep the remaining-token headers
    successes, throttled, remaining = 0, 0, []
    for _ in range(10):
        try:
            r = ask(app_a)
            successes += 1
            remaining.append(r["remaining"])
        except RateLimitError:
            throttled += 1
    # <<<
    show.kv({"succeeded": successes, "throttled": throttled, "x-remaining-tokens": remaining})

    show.step("app-b right after app-a was throttled")
    # >>> TODO 4: One call as app-b
    app_b_result = ask(app_b)
    # <<<
    show.kv(app_b_result)

    return {"a_successes": successes, "a_throttled": throttled, "a_remaining": remaining,
            "b_status": app_b_result["status"]}


if __name__ == "__main__":
    show.result(main())
