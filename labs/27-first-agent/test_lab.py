def test_conversation_memory(result):
    answer = result["v1_answer"].lower()
    assert "alex" in answer and "hr@contoso.example" in answer


def test_version_two_behaviour(result):
    assert "contoso hr" in result["v2_answer"].lower()


def test_version_pinning(result):
    assert "- contoso hr" not in result["pinned_v1"].lower()


def test_two_versions_exist(result):
    assert len(result["versions"]) >= 2
