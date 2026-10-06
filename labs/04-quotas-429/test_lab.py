def test_capacity_read(result):
    assert result["capacity"] == 1 and result["sku"]


def test_burst_hit_429(result):
    assert result["burst_throttled"] >= 1, "expected the 1K TPM deployment to throttle a burst of 8"


def test_backoff_recovers(result):
    assert result["backoff_successes"] == 2


def test_spillover_answered_everything(result):
    assert result["spillover_total"] == 4
