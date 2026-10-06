def _case(result, start):
    return next(c for c in result["cases"] if c["query"].startswith(start))


def test_tools_called_for_order_questions(result):
    assert len(_case(result, "Where is")["tool_calls"]) == 1
    assert {tc["arguments"]["order_id"] for tc in _case(result, "What happened")["tool_calls"]} == {"7710", "8812"}


def test_out_of_scope_uses_no_tools(result):
    assert _case(result, "Can you book")["tool_calls"] == []


def test_evaluators_scored_every_case(result):
    for case in result["cases"]:
        assert "intent_resolution" in case["scores"] and "task_adherence" in case["scores"]


def test_tool_call_accuracy_passes(result):
    out = _case(result, "Where is")["scores"]["tool_call_accuracy"]
    assert str(out.get("tool_call_accuracy_result", "pass")).lower() == "pass", out


def test_traced(result):
    assert all(len(c["trace_id"]) == 32 for c in result["cases"])
