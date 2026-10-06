def test_every_credit_needed_approval(result):
    for case in ("small", "large"):
        assert any(d["tool"] == "issue_credit" for d in result[case]["decisions"]), case


def test_small_credit_approved_and_applied(result):
    assert any(d["approved"] for d in result["small"]["decisions"])
    assert any(abs(e["amount"] - 150) < 0.01 for e in result["ledger"])


def test_large_credit_rejected(result):
    assert not any(d["approved"] for d in result["large"]["decisions"])
    assert all(e["amount"] <= 200 for e in result["ledger"])


def test_balance_consistent(result):
    assert abs(result["credit"] - sum(e["amount"] for e in result["ledger"])) < 0.01
