def test_invoice_fields(result):
    inv = result["invoice"]
    assert inv["currency"] == "AUD" and inv["invoice_number"] == "INV-2026-0419"
    assert len(inv["line_items"]) == 3


def test_invoice_total_consistent(result):
    assert abs(result["invoice"]["total"] - result["computed_total"]) < 0.01
    assert abs(result["computed_total"] - 3241.0) < 0.01


def test_insights_match_schema(result):
    ins = result["insights"]
    assert ins["sentiment"] in {"negative", "mixed"}
    assert ins["escalate"] is True
    assert any(e["category"] == "Person" and "Maria" in e["text"] for e in ins["entities"])


def test_json_mode_is_json(result):
    assert result["json_mode_keys"]
