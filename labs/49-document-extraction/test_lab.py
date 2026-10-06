import pytest


def test_di_prebuilt_invoice(result):
    inv = result["di"]["invoice"]
    assert inv["invoice_id"] == "FAB-20931"
    assert inv["total"] == pytest.approx(1284.00)
    assert inv["line_items"] == 3


def test_di_layout(result):
    di = result["di"]
    assert di["tables"] >= 1 and ("<table>" in di["markdown"].lower() or "|" in di["markdown"])
    assert sorted(di["selection_marks"]) == ["selected", "unselected"]


def test_cu_extract_with_confidence(result):
    cu = result["cu"]
    assert cu["fields"]["InvoiceNumber"] == "FAB-20931"
    assert cu["fields"]["TotalAmount"] == pytest.approx(1284.00)
    assert cu["confidence"]["TotalAmount"] is not None


def test_cu_classify_and_generate(result):
    f = result["cu"]["fields"]
    assert f["PaymentStatus"] == "paid"
    assert f["FollowUp"] and len(f["FollowUp"]) > 10


def test_cu_grounding(result):
    assert "InvoiceNumber" in result["cu"]["grounding"]
