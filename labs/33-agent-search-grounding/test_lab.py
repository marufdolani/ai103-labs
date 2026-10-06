def test_grounded_answer(result):
    assert "20" in result["leave"]


def test_citations_present(result):
    assert result["citations"], "the answer should carry citation annotations"


def test_security_trimming(result):
    assert "12%" not in result["bonus_staff"], "staff agent must not see the restricted bonus policy"
    assert "12" in result["bonus_hr"]
