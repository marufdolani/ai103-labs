"""Lab 22 - Multistep reasoning pipeline: extract -> compute (tool) -> draft -> verify -> fix."""
import json
from datetime import datetime

from pydantic import BaseModel

from labkit import cfg, show
from labkit.clients import openai

INCIDENT_LOG = """
2026-09-30 08:02 UTC  Alert: checkout API p95 latency > 5s (PagerDuty INC-4471)
2026-09-30 08:09 UTC  On-call (Ravi) confirms elevated 503s in West Europe
2026-09-30 08:21 UTC  Root cause suspected: config push 'cache-ttl=0' at 07:58 UTC
2026-09-30 08:34 UTC  Config rolled back by Ravi
2026-09-30 08:47 UTC  Error rate back to baseline; incident mitigated
2026-09-30 09:30 UTC  Customer comms sent; ~12% of EU checkouts failed during the window
"""
SECTIONS = ["Summary", "Timeline", "Root cause", "Impact", "Action items"]


class Event(BaseModel):
    time_utc: str
    description: str


class Facts(BaseModel):
    incident_id: str
    start_utc: str
    mitigated_utc: str
    root_cause: str
    impact: str
    timeline: list[Event]


class Verification(BaseModel):
    unsupported_claims: list[str]


def ask(model: str, instructions: str, text: str, fmt=None, effort: str = "low"):
    kwargs = {"text_format": fmt} if fmt else {}
    call = openai().responses.parse if fmt else openai().responses.create
    resp = call(model=model, instructions=instructions, input=text, reasoning={"effort": effort},
                max_output_tokens=4000, **kwargs)
    return resp.output_parsed if fmt else resp.output_text


def outage_minutes(start_utc: str, end_utc: str) -> int:
    """Deterministic tool step: never let the model do date arithmetic it can get wrong."""
    fmt = "%Y-%m-%d %H:%M"
    s, e = (datetime.strptime(x.replace(" UTC", "").replace("T", " ")[:16], fmt) for x in (start_utc, end_utc))
    return int((e - s).total_seconds() // 60)


def main() -> dict:
    # >>> TODO 1: Step 1 - extract Facts from the log with the small model (structured output)
    facts: Facts = ask(cfg("SMALL_MODEL"),
                       "Extract incident facts. Use 'YYYY-MM-DD HH:MM' for times. start_utc is the time of the FIRST "
                       "alert; mitigated_utc is when the error rate returned to baseline. Include every log line in timeline.",
                       INCIDENT_LOG, Facts)
    # <<<
    show.step("1. Facts")
    show.kv(facts.model_dump(exclude={"timeline"}))

    # >>> TODO 2: Step 2 - deterministic tool: compute outage minutes from start and mitigation times
    minutes = outage_minutes(facts.start_utc, facts.mitigated_utc)
    # <<<
    show.step(f"2. Computed outage duration: {minutes} minutes")

    # >>> TODO 3: Step 3 - draft the postmortem with the chat model using ONLY the facts + duration, with the required sections
    draft = ask(cfg("CHAT_MODEL"),
                f"Write a blameless postmortem in markdown with exactly these '##' sections: {', '.join(SECTIONS)}. "
                "Use only the facts provided; do not invent people, numbers or causes.",
                json.dumps({**facts.model_dump(), "outage_minutes": minutes}))
    # <<<

    # >>> TODO 4: Step 4 - verify with the large model: list claims in the draft not supported by the facts; Step 5 - fix once if needed
    verify_prompt = "List every claim in the DRAFT that is not supported by the FACTS. Return an empty list if none."
    check: Verification = ask(cfg("LARGE_MODEL"), verify_prompt,
                              f"FACTS:\n{facts.model_dump_json()}\noutage_minutes={minutes}\n\nDRAFT:\n{draft}", Verification)
    fixed = False
    if check.unsupported_claims:
        draft = ask(cfg("CHAT_MODEL"), "Remove or correct these unsupported claims and return the full revised markdown.",
                    f"CLAIMS:\n{check.unsupported_claims}\n\nDRAFT:\n{draft}")
        check = ask(cfg("LARGE_MODEL"), verify_prompt,
                    f"FACTS:\n{facts.model_dump_json()}\noutage_minutes={minutes}\n\nDRAFT:\n{draft}", Verification)
        fixed = True
    # <<<
    show.step("3-5. Draft verified")
    show.text("Postmortem", draft, limit=1500)
    show.kv({"unsupported claims remaining": check.unsupported_claims, "fix pass used": fixed})
    return {"facts": facts.model_dump(), "outage_minutes": minutes, "draft": draft,
            "unsupported": check.unsupported_claims, "fixed": fixed}


if __name__ == "__main__":
    show.result(main())
