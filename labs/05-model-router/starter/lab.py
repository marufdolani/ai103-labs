"""Lab 05 - Route prompts with model router."""
import time

from labkit import cfg, show
from labkit.clients import aoai

PROMPTS = {
    "lookup": "What is the capital of Australia? One word.",
    "slogan": "Write a five-word slogan for a bicycle repair shop.",
    "proof": "Prove step by step that the sum of the first n odd numbers is n squared.",
    "design": ("Design a phased migration plan for moving 40 on-premises SQL Server databases to Azure SQL, "
               "including risks, rollback and a cutover checklist."),
}


def main() -> dict:
    router = cfg("ROUTER_MODEL")
    rows = []
    for label, prompt in PROMPTS.items():
        show.step(label)
        # TODO 1: Call the router deployment with chat.completions.create and time it
        raise NotImplementedError("TODO 1: Call the router deployment with chat.completions.create and time it  (see README step and solution/ if stuck)")
        # TODO 2: Record which model answered (resp.model) and the token usage
        raise NotImplementedError("TODO 2: Record which model answered (resp.model) and the token usage  (see README step and solution/ if stuck)")
    show.table([[r["prompt"], r["routed_to"], r["latency_s"], r["prompt_tokens"], r["completion_tokens"]] for r in rows],
               ["prompt", "answered by", "sec", "in", "out"])
    return {"rows": rows, "distinct_models": sorted({r["routed_to"] for r in rows})}


if __name__ == "__main__":
    show.result(main())
