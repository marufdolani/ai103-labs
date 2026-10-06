"""Lab 13 - Groundedness and protected-material detection."""
from azure.ai.evaluation import GroundednessEvaluator

from labkit import show
from labkit.clients import Rest, RestError
from labkit.evals import REASONING_JUDGE, judge_config

GROUNDEDNESS_PATH = "contentsafety/text:detectGroundedness?api-version=2024-09-15-preview"
PROTECTED_PATH = "contentsafety/text:detectProtectedMaterial?api-version=2024-09-01"

SOURCE = ("Contoso provides 20 weeks of fully paid parental leave to the primary caregiver and 8 weeks to the "
          "secondary caregiver. Employees become eligible after 90 days of continuous service.")
QUESTION = "How much parental leave does the secondary caregiver get, and when are employees eligible?"
ANSWERS = {
    "grounded": "The secondary caregiver gets 8 weeks of paid leave, and employees are eligible after 90 days of service.",
    "fabricated": "The secondary caregiver gets 12 weeks of leave at half pay, and eligibility starts after one year.",
}


def detect_groundedness(answer: str) -> dict:
    # TODO 1: POST to detectGroundedness (QnA task) with the answer and SOURCE; return detected flag and percentage
    raise NotImplementedError("TODO 1: POST to detectGroundedness (QnA task) with the answer and SOURCE; return detected flag and percentage  (see README step and solution/ if stuck)")


def judge_groundedness(answer: str) -> float:
    # TODO 2: Score the same answer with the AI-assisted GroundednessEvaluator (1-5)
    raise NotImplementedError("TODO 2: Score the same answer with the AI-assisted GroundednessEvaluator (1-5)  (see README step and solution/ if stuck)")


def protected_material(text: str) -> bool:
    # TODO 3: POST {text} to detectProtectedMaterial and return protectedMaterialAnalysis.detected
    raise NotImplementedError("TODO 3: POST {text} to detectProtectedMaterial and return protectedMaterialAnalysis.detected  (see README step and solution/ if stuck)")


def main() -> dict:
    out = {}
    for label, answer in ANSWERS.items():
        out[label] = {"detector": detect_groundedness(answer), "judge": judge_groundedness(answer)}
    show.table([[k, v["detector"].get("ungrounded", "n/a"), v["detector"].get("ungrounded_pct", "n/a"), v["judge"]]
                for k, v in out.items()], ["answer", "ungrounded?", "ungrounded %", "judge 1-5"])
    original = "Our parental leave policy gives primary caregivers twenty paid weeks to bond with their child."
    out["protected_material_detected"] = protected_material(original)
    show.kv({"protected material in original text": out["protected_material_detected"]})
    return out


if __name__ == "__main__":
    show.result(main())
