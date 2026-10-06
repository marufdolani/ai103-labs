import pytest


def test_judge_separates_grounded_from_fabricated(result):
    assert result["grounded"]["judge"] > result["fabricated"]["judge"]


def test_detector_flags_fabrication(result):
    det = result["fabricated"]["detector"]
    if not det["supported"]:
        pytest.skip(f"Groundedness detection not available in this region: {det['error']}")
    assert det["ungrounded"] and not result["grounded"]["detector"]["ungrounded"]


def test_original_text_not_protected(result):
    assert result["protected_material_detected"] is False
