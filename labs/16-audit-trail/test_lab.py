import re


def test_trace_id_is_w3c(result):
    assert re.fullmatch(r"[0-9a-f]{32}", result["trace_id"]) and set(result["trace_id"]) != {"0"}


def test_approval_recorded_before_action(result):
    events = result["events"]
    assert "approval_decision" in events and "action_executed" in events
    assert events.index("approval_decision") < events.index("action_executed")


def test_high_value_needs_human(result):
    if result["proposed_amount"] > 100:
        assert "approval_requested" in result["events"]


def test_chain_valid_and_tamper_evident(result):
    assert result["chain_valid"] and result["tamper_detected"]
