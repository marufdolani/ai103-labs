def test_approval_was_requested(result):
    assert result["approved"]["decisions"], "require_approval='always' should produce approval requests"


def test_only_allowed_tools_requested(result):
    assert all(d["tool"] == "microsoft_docs_search" for d in result["approved"]["decisions"])


def test_approved_run_uses_docs(result):
    answer = result["approved"]["answer"].lower()
    assert "tool" in answer and ("input" in answer or "output" in answer)


def test_denied_run_executes_no_tool(result):
    assert all(not d["approved"] for d in result["denied"]["decisions"])
    assert result["denied"]["mcp_calls_in_final"] == []
