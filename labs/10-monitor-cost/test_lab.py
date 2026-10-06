def test_latency_percentiles(result):
    a = result["analytics"]
    assert 0 < a["p50_latency_s"] <= a["p95_latency_s"]


def test_cost_projection(result):
    assert result["analytics"]["usd_per_month_at_volume"] > 0


def test_platform_exposes_token_metrics(result):
    assert result["metrics"]["token_metrics"], "no token metrics found on the Foundry resource"


def test_kql_ran(result):
    assert result["log_rows"] >= 0
