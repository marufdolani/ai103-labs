def test_nine_measurements(result):
    assert len(result["rows"]) == 9
    assert all(r["latency_s"] > 0 and r["output_tokens"] > 0 for r in result["rows"])


def test_cost_computed(result):
    assert all(r["usd_per_1k_requests"] > 0 for r in result["rows"])


def test_triage_has_a_pick(result):
    assert result["triage_pick"], "no model classified the ticket correctly"


def test_high_effort_reasons_more(result):
    assert result["effort"]["high"]["reasoning_tokens"] >= result["effort"]["low"]["reasoning_tokens"]
