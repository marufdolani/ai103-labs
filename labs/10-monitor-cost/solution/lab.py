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
        # >>> TODO 1: Call CHAT_MODEL, measure latency, and capture input/output/reasoning tokens from usage
        start = time.perf_counter()
        resp = openai().responses.create(model=cfg("CHAT_MODEL"), input=q, reasoning={"effort": "low"},
                                         max_output_tokens=1500)
        latency = time.perf_counter() - start
        details = getattr(resp.usage, "output_tokens_details", None)
        rows.append({"latency_s": latency, "input": resp.usage.input_tokens, "output": resp.usage.output_tokens,
                     "reasoning": getattr(details, "reasoning_tokens", 0) or 0})
        # <<<
    return rows


def token_analytics(rows: list[dict], monthly_requests: int = 100_000) -> dict:
    # >>> TODO 2: p50/p95 latency, avg tokens, cost per request and projected monthly cost
    latencies = sorted(r["latency_s"] for r in rows)
    p95_index = max(0, int(round(0.95 * len(latencies))) - 1)
    avg_in = statistics.mean(r["input"] for r in rows)
    avg_out = statistics.mean(r["output"] for r in rows)
    cost_per_request = (avg_in * PRICE_PER_1M["input"] + avg_out * PRICE_PER_1M["output"]) / 1_000_000
    return {
        "p50_latency_s": round(statistics.median(latencies), 2),
        "p95_latency_s": round(latencies[p95_index], 2),
        "avg_input_tokens": round(avg_in, 1),
        "avg_output_tokens": round(avg_out, 1),
        "reasoning_share": round(sum(r["reasoning"] for r in rows) / max(1, sum(r["output"] for r in rows)), 2),
        "usd_per_request": round(cost_per_request, 6),
        "usd_per_month_at_volume": round(cost_per_request * monthly_requests, 2),
    }
    # <<<


def platform_metrics() -> dict:
    resource = cfg("FOUNDRY_RESOURCE_ID")
    # >>> TODO 3: List metric definitions on the Foundry resource and query the token metrics (Total, last 2 hours)
    defs = arm().get(f"{resource}/providers/microsoft.insights/metricDefinitions?api-version=2018-01-01").json()["value"]
    token_metrics = [d["name"]["value"] for d in defs if "token" in d["name"]["value"].lower()][:5]
    totals = {}
    if token_metrics:
        data = arm().get(
            f"{resource}/providers/microsoft.insights/metrics?api-version=2018-01-01"
            f"&metricnames={','.join(token_metrics)}&timespan=PT2H&interval=PT5M&aggregation=Total"
        ).json()["value"]
        for metric in data:
            totals[metric["name"]["value"]] = sum(
                (point.get("total") or 0) for series in metric.get("timeseries", []) for point in series.get("data", []))
    # <<<
    return {"token_metrics": token_metrics, "totals": totals}


def logs_query() -> int:
    # >>> TODO 4: Run a KQL query on Log Analytics over the AzureMetrics table for this resource
    client = LogsQueryClient(credential())
    kql = (f"AzureMetrics | where ResourceId =~ '{cfg('FOUNDRY_RESOURCE_ID')}' "
           "| summarize Total = sum(Total) by MetricName | order by Total desc")
    response = client.query_workspace(cfg("LOG_ANALYTICS_WORKSPACE_ID"), kql, timespan=timedelta(days=1))
    rows = [list(r) for t in response.tables for r in t.rows]
    # <<<
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
