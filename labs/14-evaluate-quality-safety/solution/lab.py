"""Lab 14 - Quality and safety evaluations, logged to the Foundry project."""
from pathlib import Path

from azure.ai.evaluation import (CoherenceEvaluator, F1ScoreEvaluator, GroundednessEvaluator, RelevanceEvaluator,
                                 SimilarityEvaluator, ViolenceEvaluator, evaluate)

from labkit import out_path, show
from labkit.clients import credential
from labkit.evals import REASONING_JUDGE, judge_config, project_endpoint

DATASET = Path(__file__).parent / "dataset.jsonl"


def build_evaluators() -> dict:
    judge = judge_config()
    # >>> TODO 1: Quality (AI-assisted), NLP (math-based) and safety evaluators
    return {
        "groundedness": GroundednessEvaluator(judge, **REASONING_JUDGE),
        "relevance": RelevanceEvaluator(judge, **REASONING_JUDGE),
        "coherence": CoherenceEvaluator(judge, **REASONING_JUDGE),
        "similarity": SimilarityEvaluator(judge, **REASONING_JUDGE),
        "f1": F1ScoreEvaluator(),
        "violence": ViolenceEvaluator(credential=credential(), azure_ai_project=project_endpoint()),
    }
    # <<<


def main() -> dict:
    # >>> TODO 2: Run evaluate() on the dataset, log to the project, and save results locally
    result = evaluate(
        data=str(DATASET),
        evaluators=build_evaluators(),
        evaluation_name="lab14-hr-assistant",
        azure_ai_project=project_endpoint(),
        output_path=str(out_path("lab14", "results.json")),
    )
    # <<<
    metrics = result["metrics"]
    show.title("Aggregate metrics")
    show.kv({k: round(v, 3) if isinstance(v, float) else v for k, v in metrics.items()})

    # >>> TODO 3: Per-row groundedness, so you can find the fabricated answer
    per_row = {row["inputs.id"]: row.get("outputs.groundedness.groundedness") for row in result["rows"]}
    # <<<
    show.title("Groundedness per row")
    show.kv(per_row)
    show.kv({"Foundry portal": result.get("studio_url") or "(see project > Evaluation)"})
    return {"metrics": metrics, "groundedness_by_row": per_row, "studio_url": result.get("studio_url")}


if __name__ == "__main__":
    show.result(main())
