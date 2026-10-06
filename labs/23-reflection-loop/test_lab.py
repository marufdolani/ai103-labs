def test_loop_is_bounded(result):
    assert 1 <= len(result["history"]) <= 3


def test_quality_does_not_regress(result):
    scores = [h["score"] for h in result["history"]]
    assert scores[-1] >= scores[0]


def test_final_email_meets_brief(result):
    email = result["final_email"]
    assert "SORRY10" in email and len(email.split()) <= 180
