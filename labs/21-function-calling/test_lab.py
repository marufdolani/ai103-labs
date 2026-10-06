def test_status_looked_up_for_both_orders(result):
    ids = {c["args"].get("order_id") for c in result["calls"] if c["name"] == "get_order_status"}
    assert {"8812", "9901"} <= ids


def test_refund_tool_used_with_enum(result):
    refunds = [c for c in result["calls"] if c["name"] == "calculate_refund"]
    assert refunds and refunds[0]["args"]["reason"] == "damaged"


def test_answer_uses_tool_results(result):
    answer = result["answer"].lower()
    assert "300" in answer and "transit" in answer


def test_loop_bounded(result):
    assert 1 <= result["rounds"] <= 5
