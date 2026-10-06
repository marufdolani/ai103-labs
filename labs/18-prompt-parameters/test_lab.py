def test_few_shot_not_worse(result):
    assert result["few_shot"] >= result["zero_shot"]
    assert result["few_shot"] >= 0.8


def test_truncation_detected(result):
    assert result["truncation"]["status"] == "incomplete"
    assert result["truncation"]["reason"] == "max_output_tokens"


def test_verbosity_changes_length(result):
    assert result["verbosity_low"] < result["verbosity_high"]


def test_temperature_lesson_recorded(result):
    temp = result["temperature"]
    assert temp["reasoning_model"].startswith(("accepted", "rejected"))
    if "distinct_at_0" in temp:
        assert temp["distinct_at_1.3"] >= temp["distinct_at_0"]
