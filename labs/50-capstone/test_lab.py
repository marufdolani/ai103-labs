def _r(result, i):
    return result["records"][i]


def test_grounded_with_citations(result):
    r = _r(result, 0)
    assert "20" in r["answer"] and r["citations"]


def test_security_trimming(result):
    assert "12%" not in _r(result, 1)["answer"]
    assert "12" in _r(result, 2)["answer"]


def test_attack_blocked_before_agent(result):
    r = _r(result, 3)
    assert r["blocked"] and "response_id" not in r


def test_action_needs_and_gets_approval(result):
    actions = _r(result, 4)["actions"]
    assert actions and actions[0]["args"]["priority"] == "P1" and actions[0]["approved"]
    assert result["tickets"] and result["tickets"][0]["id"] in _r(result, 4)["answer"]


def test_audit_log_has_provenance(result):
    assert result["audit_lines"] == 5
    assert all(r["agent_version"] and r["trace_id"] for r in result["records"])


def test_quality_gate(result):
    assert result["gate"]["release"], result["gate"]["graded"]
