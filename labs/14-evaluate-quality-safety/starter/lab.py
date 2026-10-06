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
    # TODO 1: Quality (AI-assisted), NLP (math-based) and safety evaluators
    raise NotImplementedError("TODO 1: Quality (AI-assisted), NLP (math-based) and safety evaluators  (see README step and solution/ if stuck)")


def main() -> dict:
    # TODO 2: Run evaluate() on the dataset, log to the project, and save results locally
    raise NotImplementedError("TODO 2: Run evaluate() on the dataset, log to the project, and save results locally  (see README step and solution/ if stuck)")
    metrics = result["metrics"]
    show.title("Aggregate metrics")
    show.kv({k: round(v, 3) if isinstance(v, float) else v for k, v in metrics.items()})

    # TODO 3: Per-row groundedness, so you can find the fabricated answer
    raise NotImplementedError("TODO 3: Per-row groundedness, so you can find the fabricated answer  (see README step and solution/ if stuck)")
    show.title("Groundedness per row")
    show.kv(per_row)
    show.kv({"Foundry portal": result.get("studio_url") or "(see project > Evaluation)"})
    return {"metrics": metrics, "groundedness_by_row": per_row, "studio_url": result.get("studio_url")}


if __name__ == "__main__":
    show.result(main())
