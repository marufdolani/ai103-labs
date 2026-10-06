"""Lab 03 - Choose the right model: small, large, reasoning."""
import re
import time

from labkit import cfg, show
from labkit.clients import openai

# Illustrative USD prices per 1M tokens (input, output). Check current Azure pricing for real decisions.
PRICES = {
    "nano": (0.20, 1.25),
    "mini": (0.75, 4.50),
    "large": (1.75, 14.00),
}

TASKS = {
    "triage": {
        "prompt": ("Classify this support ticket into exactly one label: billing, outage, login, feature_request. "
                   "Answer with the label only.\nTicket: 'Since 9am none of our users can reach the dashboard, we get HTTP 503.'"),
        "check": lambda a: "outage" in a.lower(),
    },
    "code": {
        "prompt": "Write a Python function is_leap_year(year: int) -> bool. Return only the code.",
        "check": lambda a: "def is_leap_year" in a and "400" in a,
    },
    "logic": {
        "prompt": ("A warehouse ships 3 pallets on Monday. Each day after, it ships twice the previous day's pallets "
                   "minus 1. On which day does the cumulative total first exceed 100 pallets? Answer with the weekday only."),
        # 3, 5, 9, 17, 33, 65 -> cumulative 3, 8, 17, 34, 67, 132 -> Saturday
        "check": lambda a: "saturday" in a.lower(),
    },
}


def tier(model: str) -> str:
    if "nano" in model:
        return "nano"
    if "mini" in model:
        return "mini"
    return "large"


def run_task(model: str, task: str, effort: str = "low") -> dict:
    """Call one model on one task and return measurements."""
    # >>> TODO 1: Time a responses.create call and collect answer + token usage (incl. reasoning tokens)
    start = time.perf_counter()
    resp = openai().responses.create(
        model=model,
        input=TASKS[task]["prompt"],
        reasoning={"effort": effort},
        max_output_tokens=4000,
    )
    latency = time.perf_counter() - start
    usage = resp.usage
    details = getattr(usage, "output_tokens_details", None)
    row = {
        "model": model,
        "task": task,
        "effort": effort,
        "answer": resp.output_text.strip(),
        "latency_s": round(latency, 2),
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "reasoning_tokens": getattr(details, "reasoning_tokens", 0) or 0,
    }
    # <<<
    # >>> TODO 2: Score the answer with TASKS[task]["check"]
    row["correct"] = bool(TASKS[task]["check"](row["answer"]))
    # <<<
    # >>> TODO 3: Cost per 1,000 requests from PRICES (USD per 1M tokens)
    price_in, price_out = PRICES[tier(model)]
    row["usd_per_1k_requests"] = round(1000 * (row["input_tokens"] * price_in + row["output_tokens"] * price_out) / 1_000_000, 4)
    # <<<
    return row


def main() -> dict:
    models = [cfg("SMALL_MODEL"), cfg("CHAT_MODEL"), cfg("LARGE_MODEL")]
    rows = []
    for task in TASKS:
        for model in models:
            show.step(f"{task} on {model}")
            rows.append(run_task(model, task))
    show.title("Benchmark")
    show.table([[r["task"], r["model"], r["correct"], r["latency_s"], r["input_tokens"], r["output_tokens"],
                 r["reasoning_tokens"], r["usd_per_1k_requests"]] for r in rows],
               ["task", "model", "ok", "sec", "in", "out", "reason", "$/1k req"])

    show.step("Reasoning effort on the small model (logic task)")
    # >>> TODO 4: Run the logic task on SMALL_MODEL with effort 'low' and 'high'
    low = run_task(cfg("SMALL_MODEL"), "logic", "low")
    high = run_task(cfg("SMALL_MODEL"), "logic", "high")
    # <<<
    show.table([[r["effort"], r["correct"], r["latency_s"], r["reasoning_tokens"]] for r in (low, high)],
               ["effort", "ok", "sec", "reasoning tokens"])

    cheapest_correct_triage = min((r for r in rows if r["task"] == "triage" and r["correct"]),
                                  key=lambda r: r["usd_per_1k_requests"], default=None)
    return {
        "rows": rows,
        "effort": {"low": low, "high": high},
        "triage_pick": cheapest_correct_triage["model"] if cheapest_correct_triage else None,
    }


if __name__ == "__main__":
    show.result(main())
