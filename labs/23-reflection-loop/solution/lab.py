"""Lab 23 - Reflection and self-critique loop (generator -> critic -> revise)."""
from pydantic import BaseModel

from labkit import cfg, show
from labkit.clients import openai

BRIEF = ("Write a customer email apologizing for the 45-minute checkout outage on 30 Sep 2026 (INC-4471) that "
         "affected ~12% of EU checkouts. Offer a 10% discount code SORRY10 valid for 30 days.")
RUBRIC = """Score 1-10. Criteria:
1. Takes responsibility without blaming individuals or vendors.
2. States the facts accurately: 45 minutes, 30 Sep 2026, ~12% of EU checkouts.
3. Includes the code SORRY10 and the 30-day validity.
4. Under 150 words, warm and plain English, no jargon such as 'p95' or 'config push'.
5. Ends with a clear next step for the customer."""


class Critique(BaseModel):
    score: int
    issues: list[str]


def generate(feedback: list[str] | None, previous: str | None) -> str:
    # >>> TODO 1: Generator: write the email; on later rounds revise `previous` to fix the critic's issues
    if previous is None:
        task = BRIEF
    else:
        task = f"Revise this email to fix ALL issues.\nISSUES:\n- " + "\n- ".join(feedback or []) + f"\n\nEMAIL:\n{previous}"
    resp = openai().responses.create(model=cfg("SMALL_MODEL"), instructions="You write customer emails for Contoso.",
                                     input=task, reasoning={"effort": "low"}, max_output_tokens=2000)
    return resp.output_text.strip()
    # <<<


def critique(email: str) -> tuple[Critique, list[str]]:
    # >>> TODO 2: Critic: a different (larger) model scores against the rubric; request a reasoning summary for transparency
    resp = openai().responses.parse(model=cfg("LARGE_MODEL"), instructions=f"You are a strict editor.\n{RUBRIC}",
                                    input=f"BRIEF:\n{BRIEF}\n\nEMAIL:\n{email}", text_format=Critique,
                                    reasoning={"effort": "medium", "summary": "auto"}, max_output_tokens=4000)
    summaries = [s.text for item in resp.output if item.type == "reasoning" for s in (item.summary or [])]
    return resp.output_parsed, summaries
    # <<<


def main(max_rounds: int = 3, target: int = 8) -> dict:
    history, email, issues, summaries = [], None, None, []
    # >>> TODO 3: Loop: generate -> critique, stop when score >= target or after max_rounds
    for round_no in range(1, max_rounds + 1):
        email = generate(issues, email)
        crit, summaries = critique(email)
        history.append({"round": round_no, "score": crit.score, "issues": crit.issues})
        show.kv({"round": round_no, "score": crit.score, "issues": "; ".join(crit.issues)[:200]})
        if crit.score >= target:
            break
        issues = crit.issues
    # <<<
    show.text("Final email", email)
    if summaries:
        show.text("Critic reasoning summary", " ".join(summaries))
    return {"history": history, "final_email": email, "reasoning_summary": " ".join(summaries)}


if __name__ == "__main__":
    show.result(main())
