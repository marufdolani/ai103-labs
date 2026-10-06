"""Lab 24 - Hybrid LLM + rules engine with multi-model orchestration."""
from typing import Literal, Optional

from pydantic import BaseModel

from labkit import cfg, show
from labkit.clients import openai

TIER1 = {"new york", "london", "tokyo", "sydney"}
CLAIMS = {
    "C1": "Flew Sydney to Tokyo (9.5 hour flight) in business class, director approval DA-221 attached, fare USD 4,200, receipt attached.",
    "C2": "Business class Melbourne to Sydney, 1.5 hour flight, USD 900, receipt attached. No approval needed I think.",
    "C3": "Hotel in Tokyo for 3 nights at USD 310 per night, receipts attached.",
    "C4": "Dinner with a client in Denver, total USD 70 including a USD 15 glass of wine. Receipt attached.",
    "C5": "Gift hampers for our top client, total USD 7,000, receipt attached.",
}
EXPECTED = {"C1": "approve", "C2": "reject", "C3": "reject", "C4": "approve", "C5": "escalate"}


class Claim(BaseModel):
    category: Literal["flight", "hotel", "meal", "other"]
    amount_usd: float
    flight_hours: Optional[float]
    cabin: Literal["economy", "business", "none"]
    has_director_approval: bool
    city: Optional[str]
    nights: Optional[int]
    nightly_rate_usd: Optional[float]
    alcohol_usd: float
    has_receipt: bool
    confidence: float


def extract(text: str, model: str) -> Claim:
    # TODO 1: LLM step: extract a Claim (structured output) and self-rate confidence 0-1
    raise NotImplementedError("TODO 1: LLM step: extract a Claim (structured output) and self-rate confidence 0-1  (see README step and solution/ if stuck)")


def extract_with_escalation(text: str) -> tuple[Claim, str]:
    # TODO 2: Orchestration: small model first; if confidence < 0.7 re-extract with the large model
    raise NotImplementedError("TODO 2: Orchestration: small model first; if confidence < 0.7 re-extract with the large model  (see README step and solution/ if stuck)")


def apply_policy(c: Claim) -> dict:
    """Deterministic rules engine for POL-FIN-004. The LLM never decides."""
    # TODO 3: Implement the policy: CFO escalation > 5,000; business class needs >= 6h AND approval;
    raise NotImplementedError("TODO 3: Implement the policy: CFO escalation > 5,000; business class needs >= 6h AND approval;  (see README step and solution/ if stuck)")


def explain(text: str, decision: dict) -> str:
    resp = openai().responses.create(model=cfg("CHAT_MODEL"), reasoning={"effort": "low"}, max_output_tokens=800,
                                     instructions="Explain the decision to the employee in one friendly sentence. Do not change it.",
                                     input=f"Claim: {text}\nDecision: {decision}")
    return resp.output_text.strip()


def main() -> dict:
    results = {}
    for cid, text in CLAIMS.items():
        claim, model_used = extract_with_escalation(text)
        decision = apply_policy(claim)
        results[cid] = {**decision, "extracted_by": model_used, "confidence": claim.confidence,
                        "message": explain(text, decision)}
    show.table([[k, v["decision"], v["approved_usd"], v["rule"], v["extracted_by"]] for k, v in results.items()],
               ["claim", "decision", "approved", "rule", "extracted by"])
    return {"results": results, "expected": EXPECTED}


if __name__ == "__main__":
    show.result(main())
