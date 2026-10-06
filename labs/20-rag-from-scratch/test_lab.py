def test_chunks_indexed(result):
    assert result["chunks"] >= 6


def test_semantic_hybrid_finds_everything(result):
    for question, expected in result["expected"].items():
        assert result["top1"][question]["semantic"] == expected, question


def test_keyword_finds_exact_identifier(result):
    assert result["top1"]["What is policy POL-IT-009 about?"]["keyword"] == "POL-IT-009"


def test_answer_is_cited(result):
    assert "[POL-HR-017]" in result["answer"]
    assert "20" in result["answer"]
