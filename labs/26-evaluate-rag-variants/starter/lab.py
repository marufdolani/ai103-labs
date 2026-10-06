"""Lab 26 - Evaluate and compare RAG variants (A/B) to choose what ships."""
from azure.ai.evaluation import GroundednessEvaluator, ResponseCompletenessEvaluator, RetrievalEvaluator

from labkit import cfg, show
from labkit.clients import openai, search_client
from labkit.evals import REASONING_JUDGE, judge_config
from labkit.rag import INDEX_NAME, ensure_policy_index, format_context, hybrid_search

QUESTIONS = [
    ("Can new parents take time off, and how much?", "Primary caregivers get 20 weeks of fully paid parental leave; secondary caregivers get 8 weeks."),
    ("What's the nightly hotel limit when I travel to London?", "USD 250 per night in tier-1 cities such as London."),
    ("How long before my laptop gets replaced?", "Every 3 years, or after 2 years for engineers whose builds exceed 10 minutes."),
    ("I clicked a dodgy link in an email. What now?", "Report suspected phishing to security@contoso.example within 1 hour."),
    ("Can I work from Portugal for a month?", "Working from another country is allowed for up to 20 working days per year with HR and tax approval."),
]


def retrieve_a(question: str) -> list[dict]:
    """Variant A: keyword-only, top 1."""
    # TODO 1: Plain keyword search, top=1
    raise NotImplementedError("TODO 1: Plain keyword search, top=1  (see README step and solution/ if stuck)")


def retrieve_b(question: str) -> list[dict]:
    """Variant B: hybrid + semantic ranker, top 4."""
    # TODO 2: Use labkit.rag.hybrid_search with top=4
    raise NotImplementedError("TODO 2: Use labkit.rag.hybrid_search with top=4  (see README step and solution/ if stuck)")


def generate(question: str, context: str) -> str:
    resp = openai().responses.create(model=cfg("CHAT_MODEL"), reasoning={"effort": "low"}, max_output_tokens=1500,
                                     instructions="Answer only from the sources. Say 'I don't know' if they don't cover it.",
                                     input=f"SOURCES:\n{context}\n\nQUESTION: {question}")
    return resp.output_text


def evaluate_variant(retriever) -> dict:
    judge = judge_config()
    groundedness = GroundednessEvaluator(judge, **REASONING_JUDGE)
    retrieval = RetrievalEvaluator(judge, **REASONING_JUDGE)
    completeness = ResponseCompletenessEvaluator(judge, **REASONING_JUDGE)
    scores = {"groundedness": [], "retrieval": [], "completeness": []}
    for question, truth in QUESTIONS:
        context = format_context(retriever(question))
        answer = generate(question, context)
        # TODO 3: Score groundedness (query, context, response), retrieval (query, context), completeness (response, ground_truth)
        raise NotImplementedError("TODO 3: Score groundedness (query, context, response), retrieval (query, context), completeness (response, ground_truth)  (see README step and solution/ if stuck)")
    return {k: round(sum(v) / len(v), 2) for k, v in scores.items()}


def main() -> dict:
    ensure_policy_index()
    a, b = evaluate_variant(retrieve_a), evaluate_variant(retrieve_b)
    show.table([[m, a[m], b[m]] for m in a], ["metric (1-5)", "A: keyword top-1", "B: hybrid+semantic top-4"])
    winner = "B" if sum(b.values()) >= sum(a.values()) else "A"
    show.ok(f"Ship variant {winner}")
    return {"A": a, "B": b, "winner": winner}


if __name__ == "__main__":
    show.result(main())
