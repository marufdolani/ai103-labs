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
    # TODO 1: Generator: write the email; on later rounds revise `previous` to fix the critic's issues
    raise NotImplementedError("TODO 1: Generator: write the email; on later rounds revise `previous` to fix the critic's issues  (see README step and solution/ if stuck)")


def critique(email: str) -> tuple[Critique, list[str]]:
    # TODO 2: Critic: a different (larger) model scores against the rubric; request a reasoning summary for transparency
    raise NotImplementedError("TODO 2: Critic: a different (larger) model scores against the rubric; request a reasoning summary for transparency  (see README step and solution/ if stuck)")


def main(max_rounds: int = 3, target: int = 8) -> dict:
    history, email, issues, summaries = [], None, None, []
    # TODO 3: Loop: generate -> critique, stop when score >= target or after max_rounds
    raise NotImplementedError("TODO 3: Loop: generate -> critique, stop when score >= target or after max_rounds  (see README step and solution/ if stuck)")
    show.text("Final email", email)
    if summaries:
        show.text("Critic reasoning summary", " ".join(summaries))
    return {"history": history, "final_email": email, "reasoning_summary": " ".join(summaries)}


if __name__ == "__main__":
    show.result(main())
