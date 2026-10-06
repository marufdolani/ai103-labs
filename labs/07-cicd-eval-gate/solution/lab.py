"""Lab 07 - CI/CD for Foundry with an evaluation gate.

Run locally with ./lab run 07, or in GitHub Actions:  python labs/07-cicd-eval-gate/solution/lab.py --gate
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))  # repo root, so the workflow can run this file directly

from azure.ai.evaluation import GroundednessEvaluator, RelevanceEvaluator  # noqa: E402

from labkit import cfg, show  # noqa: E402
from labkit.clients import openai  # noqa: E402
from labkit.evals import REASONING_JUDGE, judge_config  # noqa: E402


def load_rows() -> list[dict]:
    return [json.loads(l) for l in (HERE / "eval_set.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def answer(system_prompt: str, row: dict) -> str:
    """The 'application under test': answers a question from supplied context."""
    # >>> TODO 1: Call CHAT_MODEL with instructions=system_prompt and input containing CONTEXT and QUESTION
    resp = openai().responses.create(
        model=cfg("CHAT_MODEL"),
        instructions=system_prompt,
        input=f"CONTEXT:\n{row['context']}\n\nQUESTION: {row['query']}",
        reasoning={"effort": "low"},
        max_output_tokens=1500,
    )
    return resp.output_text.strip()
    # <<<


def evaluate_prompt(prompt_file: str) -> dict:
    system_prompt = (HERE / prompt_file).read_text(encoding="utf-8")
    groundedness = GroundednessEvaluator(judge_config(), **REASONING_JUDGE)
    relevance = RelevanceEvaluator(judge_config(), **REASONING_JUDGE)
    scores = {"groundedness": [], "relevance": [], "contains": []}
    for row in load_rows():
        response = answer(system_prompt, row)
        # >>> TODO 2: Score each response with both evaluators and a deterministic must_contain check
        g = groundedness(query=row["query"], context=row["context"], response=response)
        r = relevance(query=row["query"], response=response)
        scores["groundedness"].append(float(g["groundedness"]))
        scores["relevance"].append(float(r["relevance"]))
        scores["contains"].append(1.0 if row["must_contain"].lower() in response.lower() else 0.0)
        # <<<
    return {
        "groundedness_mean": sum(scores["groundedness"]) / len(scores["groundedness"]),
        "relevance_mean": sum(scores["relevance"]) / len(scores["relevance"]),
        "contains_rate": sum(scores["contains"]) / len(scores["contains"]),
    }


def gate(metrics: dict) -> tuple[bool, list[str]]:
    thresholds = json.loads((HERE / "gate.json").read_text(encoding="utf-8"))
    # >>> TODO 3: Compare every metric with its threshold; return (passed, list of failure messages)
    failures = [f"{k}={metrics[k]:.2f} < {v}" for k, v in thresholds.items() if metrics[k] < v]
    return not failures, failures
    # <<<


def main() -> dict:
    out = {}
    for variant in ("prompt_good.txt", "prompt_bad.txt"):
        show.step(f"Evaluating {variant}")
        metrics = evaluate_prompt(variant)
        passed, failures = gate(metrics)
        show.kv({**{k: round(v, 2) for k, v in metrics.items()}, "gate": "PASS" if passed else f"FAIL {failures}"})
        out[variant.split(".")[0]] = {"metrics": metrics, "passed": passed}
    return out


if __name__ == "__main__":
    if "--gate" in sys.argv:
        metrics = evaluate_prompt("prompt_good.txt")
        passed, failures = gate(metrics)
        print(json.dumps(metrics, indent=2))
        print("GATE PASSED" if passed else f"GATE FAILED: {failures}")
        sys.exit(0 if passed else 1)
    show.result(main())
