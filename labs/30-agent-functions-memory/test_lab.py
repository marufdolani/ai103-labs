def test_tools_were_used(result):
    assert {"get_leave_balance", "remember_preference", "recall_preferences"} <= set(result["calls"])


def test_preference_persisted(result):
    prefs = result["memory"].get("E-1001", {})
    assert any("sam" in str(v).lower() for v in prefs.values())


def test_short_term_answer(result):
    assert "14" in result["answer1"]


def test_long_term_memory_across_conversations(result):
    assert "sam" in result["answer2"].lower() and "6" in result["answer2"]
