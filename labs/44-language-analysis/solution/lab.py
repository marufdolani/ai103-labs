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
    # >>> TODO 1: Keyless TextAnalyticsClient on the Foundry resource endpoint
    return TextAnalyticsClient(endpoint=cfg("FOUNDRY_ENDPOINT"), credential=credential())
    # <<<


def language_service() -> dict:
    client = language_client()
    # >>> TODO 2: Detect language, then sentiment WITH opinion mining (aspect-level), then entities and key phrases
    languages = [d.primary_language.iso6391_name for d in client.detect_language(REVIEWS)]
    sentiment = client.analyze_sentiment([REVIEWS[0]], show_opinion_mining=True)[0]
    opinions = [{"target": o.target.text, "sentiment": o.target.sentiment,
                 "assessments": [a.text for a in o.assessments]}
                for s in sentiment.sentences for o in s.mined_opinions]
    entities = [{"text": e.text, "category": e.category, "confidence": round(e.confidence_score, 2)}
                for e in client.recognize_entities([REVIEWS[0]])[0].entities]
    key_phrases = client.extract_key_phrases([REVIEWS[0]])[0].key_phrases
    # <<<
    # >>> TODO 3: Detect and redact PII in the support ticket
    pii = client.recognize_pii_entities([TICKET])[0]
    redacted, pii_categories = pii.redacted_text, sorted({e.category for e in pii.entities})
    # <<<
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
    # >>> TODO 4: Same review through an LLM with structured outputs: tone (nuance the service doesn't score) + topics
    review = openai().responses.parse(
        model=cfg("CHAT_MODEL"), reasoning={"effort": "low"}, max_output_tokens=2000, text_format=ReviewInsight,
        instructions="Extract insight from a customer review. Use ISO 639-1 for language.",
        input=REVIEWS[0]).output_parsed
    # <<<
    # >>> TODO 5: Domain customisation: compliance summarisation that keeps ONLY obligations, deadlines and risk
    compliance = openai().responses.parse(
        model=cfg("CHAT_MODEL"), reasoning={"effort": "low"}, max_output_tokens=2000, text_format=ComplianceSummary,
        instructions=("You are a compliance analyst. Extract only regulatory or contractual obligations and their "
                      "deadlines. Ignore social or logistical content. risk_level is low, medium or high."),
        input=COMPLIANCE_NOTE).output_parsed
    # <<<
    return {"review": review.model_dump(), "compliance": compliance.model_dump()}


def safety() -> dict:
    # >>> TODO 6: Content Safety text analysis: severity per harm category for a threatening message
    body = Rest().post("contentsafety/text:analyze?api-version=2024-09-01",
                       {"text": HARMFUL, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
                        "outputType": "FourSeverityLevels"}).json()
    return {c["category"]: c["severity"] for c in body["categoriesAnalysis"]}
    # <<<


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
