"""Lab 25 - Fine-tuning: decide, prepare data (SFT + DPO), validate, upload, optionally submit."""
import json
import os
import time
from pathlib import Path

from labkit import out_path, show
from labkit.clients import aoai

HERE = Path(__file__).parent
SYSTEM = "Rewrite customer messages in Contoso's voice: warm, plain English, short, no jargon."

# Which optimisation technique fits each scenario? (prompting | rag | sft | dpo | rft)
SCENARIOS = {
    "Answers must reflect HR policies that change every week": None,
    "Consistent brand voice; few-shot prompt already 3,000 tokens per call": None,
    "We have pairs of preferred vs rejected replies from human reviewers": None,
    "Improve a reasoning model on graded maths tasks with an automatic grader": None,
    "Model ignores the output format until we add two examples": None,
}


def choose_techniques() -> dict:
    # >>> TODO 1: Map each scenario to prompting, rag, sft, dpo or rft
    return dict(zip(SCENARIOS, ["rag", "sft", "dpo", "rft", "prompting"]))
    # <<<


def build_sft(path: Path) -> int:
    rows = [json.loads(l) for l in (HERE / "sft_examples.jsonl").read_text(encoding="utf-8").splitlines()]
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            # >>> TODO 2: Chat-format SFT record: system, user (source) and assistant (target) messages
            record = {"messages": [{"role": "system", "content": SYSTEM},
                                   {"role": "user", "content": r["source"]},
                                   {"role": "assistant", "content": r["target"]}]}
            # <<<
            f.write(json.dumps(record) + "\n")
    return len(rows)


def build_dpo(path: Path) -> int:
    rows = [json.loads(l) for l in (HERE / "dpo_examples.jsonl").read_text(encoding="utf-8").splitlines()]
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            # >>> TODO 3: DPO record: input.messages, preferred_output and non_preferred_output (assistant messages)
            record = {"input": {"messages": [{"role": "system", "content": SYSTEM},
                                             {"role": "user", "content": r["source"]}]},
                      "preferred_output": [{"role": "assistant", "content": r["preferred"]}],
                      "non_preferred_output": [{"role": "assistant", "content": r["rejected"]}]}
            # <<<
            f.write(json.dumps(record) + "\n")
    return len(rows)


def validate_sft(path: Path) -> list[str]:
    # >>> TODO 4: Validate: >= 10 examples, valid JSON, roles in order system/user/assistant, non-empty content, < 4k chars each
    errors = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 10:
        errors.append(f"need at least 10 examples, found {len(lines)}")
    for i, line in enumerate(lines, 1):
        try:
            msgs = json.loads(line)["messages"]
        except (json.JSONDecodeError, KeyError):
            errors.append(f"line {i}: not a messages record")
            continue
        if [m["role"] for m in msgs] != ["system", "user", "assistant"]:
            errors.append(f"line {i}: roles must be system,user,assistant")
        if any(not m["content"].strip() for m in msgs) or len(line) > 4000:
            errors.append(f"line {i}: empty or too long")
    return errors
    # <<<


def upload(path: Path) -> dict:
    # >>> TODO 5: Upload with purpose 'fine-tune' and wait until the file is processed
    f = aoai().files.create(file=path.open("rb"), purpose="fine-tune")
    for _ in range(60):
        f = aoai().files.retrieve(f.id)
        if f.status in ("processed", "error"):
            break
        time.sleep(5)
    return {"id": f.id, "status": f.status}
    # <<<


def main() -> dict:
    techniques = choose_techniques()
    show.title("Which technique?")
    show.kv(techniques)

    sft_path, dpo_path = out_path("lab25", "train_sft.jsonl"), out_path("lab25", "train_dpo.jsonl")
    n_sft, n_dpo = build_sft(sft_path), build_dpo(dpo_path)
    errors = validate_sft(sft_path)
    show.kv({"SFT examples": n_sft, "DPO examples": n_dpo, "validation errors": errors or "none"})

    uploaded = upload(sft_path)
    show.kv({"uploaded file": uploaded})
    job = None
    if os.environ.get("RUN_FINE_TUNE", "").lower() == "true":  # costs money: opt in explicitly
        job = aoai().fine_tuning.jobs.create(model=os.environ.get("FT_BASE_MODEL", "gpt-4.1-mini-2025-04-14"),
                                             training_file=uploaded["id"], suffix="contoso-voice")
        show.kv({"fine-tuning job": job.id, "status": job.status})
    return {"techniques": techniques, "sft_count": n_sft, "dpo_count": n_dpo, "errors": errors,
            "file": uploaded, "job_id": getattr(job, "id", None)}


def cleanup() -> None:
    for f in aoai().files.list(purpose="fine-tune"):
        if f.filename.startswith("train_"):
            aoai().files.delete(f.id)


if __name__ == "__main__":
    show.result(main())
