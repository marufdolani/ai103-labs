def test_decisions_follow_policy(result):
    for cid, expected in result["expected"].items():
        assert result["results"][cid]["decision"] == expected, (cid, result["results"][cid])


def test_alcohol_removed(result):
    assert abs(result["results"]["C4"]["approved_usd"] - 55.0) < 0.01


def test_explanations_written(result):
    assert all(len(r["message"]) > 10 for r in result["results"].values())
