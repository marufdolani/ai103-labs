def test_better_retrieval_wins(result):
    assert result["B"]["retrieval"] >= result["A"]["retrieval"]
    assert result["B"]["completeness"] >= result["A"]["completeness"]


def test_winner_declared(result):
    assert result["winner"] == "B"
