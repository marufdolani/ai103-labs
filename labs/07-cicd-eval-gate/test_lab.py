def test_good_prompt_passes_gate(result):
    assert result["prompt_good"]["passed"], result["prompt_good"]["metrics"]


def test_bad_prompt_is_blocked(result):
    assert not result["prompt_bad"]["passed"], "the gate must catch the regressed prompt"


def test_metrics_in_range(result):
    for variant in result.values():
        m = variant["metrics"]
        assert 1 <= m["groundedness_mean"] <= 5 and 1 <= m["relevance_mean"] <= 5
