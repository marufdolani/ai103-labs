def test_billing_routed_to_billing(result):
    authors = {r["author"] for r in result["billing_case"]}
    assert "billing" in authors and "tech" not in authors


def test_tech_routed_to_tech(result):
    authors = {r["author"] for r in result["tech_case"]}
    assert "tech" in authors and "billing" not in authors


def test_group_chat_both_spoke(result):
    authors = {r["author"] for r in result["group_chat"]}
    assert {"writer", "critic"} <= authors


def test_magentic_answer(result):
    assert result["magentic"] and "content understanding" in result["magentic"][-1]["text"].lower()
