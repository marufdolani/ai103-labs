"""Lab 44 - Text analysis: Azure Language (deterministic, scored) vs an LLM (flexible, schema-bound)."""
from azure.ai.textanalytics import TextAnalyticsClient
from pydantic import BaseModel

from labkit import cfg, show
from labkit.clients import Rest, credential, openai

REVIEWS = [
    "The food at Contoso Cafe in Seattle was excellent, but the service was painfully slow and the staff were rude.",
    "Le personnel de l'hôtel Contoso à Lyon était très accueillant et la chambre impeccable.",
    "コントソのサポートチームはとても親切で、問題をすぐに解決してくれました。",
]
TICKET = ("Hi, I'm Maria Garcia. Please call me on 555-0134 or email maria.garcia@example.com about invoice "
          "INV-2207. My card ending 4421 was charged twice on 3 October.")
COMPLIANCE_NOTE = (
    "Internal memo: The Q3 vendor review found that two suppliers stored customer data outside the approved region. "
    "Remediation is due by 15 November. Legal must be informed of any further breach within 72 hours. "
    "The team also discussed the office party budget and parking arrangements.")
HARMFUL = "I will hurt you if you post that review again."


def language_client() -> TextAnalyticsClient:
    # TODO 1: Keyless TextAnalyticsClient on the Foundry resource endpoint
    raise NotImplementedError("TODO 1: Keyless TextAnalyticsClient on the Foundry resource endpoint  (see README step and solution/ if stuck)")


def language_service() -> dict:
    client = language_client()
    # TODO 2: Detect language, then sentiment WITH opinion mining (aspect-level), then entities and key phrases
    raise NotImplementedError("TODO 2: Detect language, then sentiment WITH opinion mining (aspect-level), then entities and key phrases  (see README step and solution/ if stuck)")
    # TODO 3: Detect and redact PII in the support ticket
    raise NotImplementedError("TODO 3: Detect and redact PII in the support ticket  (see README step and solution/ if stuck)")
    return {"languages": languages, "overall_sentiment": sentiment.sentiment, "opinions": opinions,
            "entities": entities, "key_phrases": key_phrases, "redacted": redacted, "pii_categories": pii_categories}


class ReviewInsight(BaseModel):
    language: str
    tone: str                    # e.g. angry, delighted, neutral, sarcastic
    entities: list[str]
    complaint_topics: list[str]
    summary: str


class ComplianceSummary(BaseModel):
    obligations: list[str]
    deadlines: list[str]
    risk_level: str              # low | medium | high


def llm_extraction() -> dict:
    # TODO 4: Same review through an LLM with structured outputs: tone (nuance the service doesn't score) + topics
    raise NotImplementedError("TODO 4: Same review through an LLM with structured outputs: tone (nuance the service doesn't score) + topics  (see README step and solution/ if stuck)")
    # TODO 5: Domain customisation: compliance summarisation that keeps ONLY obligations, deadlines and risk
    raise NotImplementedError("TODO 5: Domain customisation: compliance summarisation that keeps ONLY obligations, deadlines and risk  (see README step and solution/ if stuck)")
    return {"review": review.model_dump(), "compliance": compliance.model_dump()}


def safety() -> dict:
    # TODO 6: Content Safety text analysis: severity per harm category for a threatening message
    raise NotImplementedError("TODO 6: Content Safety text analysis: severity per harm category for a threatening message  (see README step and solution/ if stuck)")


def main() -> dict:
    show.title("Azure Language (Foundry Tools)")
    lang = language_service()
    show.kv({"languages": lang["languages"], "overall sentiment": lang["overall_sentiment"]})
    show.table([[o["target"], o["sentiment"], ", ".join(o["assessments"])] for o in lang["opinions"]],
               ["aspect", "sentiment", "assessments"])
    show.table([[e["text"], e["category"], e["confidence"]] for e in lang["entities"]], ["entity", "category", "conf."])
    show.text("PII redacted", lang["redacted"])

    show.title("LLM with structured outputs")
    llm = llm_extraction()
    show.kv(llm["review"])
    show.kv(llm["compliance"])

    show.title("Content Safety: harm severity (0 safe, 2 low, 4 medium, 6 high)")
    sev = safety()
    show.kv(sev)
    return {"language": lang, "llm": llm, "safety": sev}


if __name__ == "__main__":
    show.result(main())
