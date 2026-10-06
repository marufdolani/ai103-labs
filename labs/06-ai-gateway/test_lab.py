def test_gateway_forwards_with_managed_identity(result):
    assert result["a_successes"] >= 1


def test_token_limit_enforced(result):
    assert result["a_throttled"] >= 1, "app-a should exceed its tokens-per-minute budget"


def test_remaining_tokens_header(result):
    assert any(r is not None for r in result["a_remaining"])


def test_other_consumer_unaffected(result):
    assert result["b_status"] == 200
