"""Lab 10 - Monitor tokens, latency, drift and cost."""
import statistics
import time
from datetime import timedelta

from azure.monitor.query import LogsQueryClient

from labkit import cfg, show
from labkit.clients import arm, credential, openai

PRICE_PER_1M = {"input": 0.75, "output": 4.50}  # illustrative mini-model prices (USD)
QUESTIONS = [
    "Summarize the benefits of keyless authentication in two sentences.",
    "List three causes of HTTP 429 errors on model deployments.",
    "What is a private endpoint? One sentence.",
    "Give one tip to reduce token usage in prompts.",
    "Explain groundedness in one sentence.",
    "What is model router? One sentence.",
]


def generate_traffic() -> list[dict]:
    rows = []
    for q in QUESTIONS:
        # TODO 1: Call CHAT_MODEL, measure latency, and capture input/output/reasoning tokens from usage
        raise NotImplementedError("TODO 1: Call CHAT_MODEL, measure latency, and capture input/output/reasoning tokens from usage  (see README step and solution/ if stuck)")
    return rows


def token_analytics(rows: list[dict], monthly_requests: int = 100_000) -> dict:
    # TODO 2: p50/p95 latency, avg tokens, cost per request and projected monthly cost
    raise NotImplementedError("TODO 2: p50/p95 latency, avg tokens, cost per request and projected monthly cost  (see README step and solution/ if stuck)")


def platform_metrics() -> dict:
    resource = cfg("FOUNDRY_RESOURCE_ID")
    # TODO 3: List metric definitions on the Foundry resource and query the token metrics (Total, last 2 hours)
    raise NotImplementedError("TODO 3: List metric definitions on the Foundry resource and query the token metrics (Total, last 2 hours)  (see README step and solution/ if stuck)")
    return {"token_metrics": token_metrics, "totals": totals}


def logs_query() -> int:
    # TODO 4: Run a KQL query on Log Analytics over the AzureMetrics table for this resource
    raise NotImplementedError("TODO 4: Run a KQL query on Log Analytics over the AzureMetrics table for this resource  (see README step and solution/ if stuck)")
    show.table(rows[:10] or [["(no rows yet: diagnostic export lags ~10 minutes)", ""]], ["metric", "total"])
    return len(rows)


def main() -> dict:
    show.step("Generating traffic")
    rows = generate_traffic()
    analytics = token_analytics(rows)
    show.title("Client-side token analytics")
    show.kv(analytics)

    show.title("Azure Monitor platform metrics")
    metrics = platform_metrics()
    show.kv(metrics["totals"] or {"metrics": metrics["token_metrics"]})

    show.title("Log Analytics (KQL)")
    log_rows = logs_query()
    return {"analytics": analytics, "metrics": metrics, "log_rows": log_rows}


if __name__ == "__main__":
    show.result(main())
