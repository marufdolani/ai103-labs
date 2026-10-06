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
    # >>> TODO 1: LLM step: extract a Claim (structured output) and self-rate confidence 0-1
    resp = openai().responses.parse(model=model, input=text, text_format=Claim, reasoning={"effort": "low"},
                                    instructions=("Extract the expense claim. Use 0 for alcohol_usd if none, null for unknown "
                                                  "numbers. confidence = how sure you are every field is correct (0-1)."),
                                    max_output_tokens=3000)
    return resp.output_parsed
    # <<<


def extract_with_escalation(text: str) -> tuple[Claim, str]:
    # >>> TODO 2: Orchestration: small model first; if confidence < 0.7 re-extract with the large model
    claim = extract(text, cfg("SMALL_MODEL"))
    if claim.confidence < 0.7:
        return extract(text, cfg("LARGE_MODEL")), cfg("LARGE_MODEL")
    return claim, cfg("SMALL_MODEL")
    # <<<


def apply_policy(c: Claim) -> dict:
    """Deterministic rules engine for POL-FIN-004. The LLM never decides."""
    # >>> TODO 3: Implement the policy: CFO escalation > 5,000; business class needs >= 6h AND approval;
    #             hotel cap 250 (tier-1) / 180; alcohol not reimbursable; receipts required above 25
    if c.amount_usd > 5000:
        return {"decision": "escalate", "approved_usd": 0, "rule": "Claims over USD 5,000 need CFO approval"}
    if c.amount_usd > 25 and not c.has_receipt:
        return {"decision": "reject", "approved_usd": 0, "rule": "Itemized receipt required above USD 25"}
    if c.category == "flight" and c.cabin == "business":
        if (c.flight_hours or 0) < 6:
            return {"decision": "reject", "approved_usd": 0, "rule": "Economy required for flights under 6 hours"}
        if not c.has_director_approval:
            return {"decision": "reject", "approved_usd": 0, "rule": "Business class needs director approval"}
    if c.category == "hotel":
        cap = 250 if (c.city or "").lower() in TIER1 else 180
        if (c.nightly_rate_usd or 0) > cap:
            return {"decision": "reject", "approved_usd": 0, "rule": f"Hotel cap USD {cap}/night"}
    approved = round(c.amount_usd - (c.alcohol_usd or 0), 2)
    return {"decision": "approve", "approved_usd": approved,
            "rule": "Alcohol removed" if c.alcohol_usd else "Within policy"}
    # <<<


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
