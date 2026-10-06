def test_fabricated_row_scores_lowest(result):
    scores = {k: float(v) for k, v in result["groundedness_by_row"].items() if v is not None}
    assert min(scores, key=scores.get) == "q4", scores


def test_quality_and_nlp_metrics_present(result):
    keys = " ".join(result["metrics"])
    for name in ("groundedness", "relevance", "coherence", "similarity", "f1"):
        assert name in keys, f"missing {name} metric"


def test_safety_metric_present(result):
    assert any("violence" in k for k in result["metrics"])
