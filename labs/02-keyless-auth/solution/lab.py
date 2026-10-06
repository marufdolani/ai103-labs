"""Lab 02 - Keyless access with Entra ID and disabled keys."""
import base64
import json

import requests

from labkit import cfg, show
from labkit.clients import COGNITIVE_SCOPE, aoai, arm, arm_path, credential


def decode_claims(jwt: str) -> dict:
    """Decode (not validate) the payload of a JWT so we can inspect it."""
    payload = jwt.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


def main() -> dict:
    show.step("1. Entra ID token for Foundry Tools")
    # >>> TODO 1: Get a token for COGNITIVE_SCOPE with credential() and decode its claims
    access_token = credential().get_token(COGNITIVE_SCOPE).token
    claims = decode_claims(access_token)
    # <<<
    show.kv({"aud": claims.get("aud"), "oid": claims.get("oid"), "tid": claims.get("tid"),
             "identity": claims.get("upn") or claims.get("appid") or claims.get("app_displayname")})

    show.step("2. Keyless model call (token provider instead of api_key)")
    # >>> TODO 2: Call the SMALL_MODEL deployment with aoai().responses.create and keep output_text
    resp = aoai().responses.create(
        model=cfg("SMALL_MODEL"),
        input="Reply with exactly: keyless works",
        reasoning={"effort": "low"},
        max_output_tokens=300,
    )
    keyless_answer = resp.output_text
    # <<<
    show.ok(keyless_answer.strip())

    show.step("3. Key-based call (should be refused)")
    # >>> TODO 3: POST to <FOUNDRY_OPENAI_ENDPOINT>/openai/v1/responses with an 'api-key' header; record the status code
    url = f"{cfg('FOUNDRY_OPENAI_ENDPOINT').rstrip('/')}/openai/v1/responses"
    r = requests.post(url, headers={"api-key": "0" * 32, "Content-Type": "application/json"},
                      json={"model": cfg("SMALL_MODEL"), "input": "hi"}, timeout=60)
    key_status = r.status_code
    # <<<
    show.warn(f"HTTP {key_status}: {r.text[:160]}")

    show.step("4. Resource configuration (control plane)")
    # >>> TODO 4: GET the Foundry resource from ARM and read properties.disableLocalAuth
    account = arm().get(arm_path(cfg("FOUNDRY_RESOURCE_ID"))).json()
    disable_local_auth = bool(account["properties"].get("disableLocalAuth"))
    # <<<
    show.kv({"disableLocalAuth": disable_local_auth, "customSubDomainName": account["properties"].get("customSubDomainName")})

    return {
        "audience": str(claims.get("aud", "")),
        "keyless_answer": keyless_answer,
        "key_status": key_status,
        "disable_local_auth": disable_local_auth,
    }


if __name__ == "__main__":
    show.result(main())
