def test_prebuilt_returns_markdown(result):
    assert len(result["prebuilt_markdown"]) > 20


def test_classify_field(result):
    assert result["image_fields"]["ChartType"] == "pie"


def test_generate_fields(result):
    f = result["image_fields"]
    assert f["KeyInsight"] and f["AltText"] and len(f["AltText"]) <= 160


def test_video_segments(result):
    segs = result["segments"]
    assert segs and all(s["end_ms"] is not None for s in segs)
    assert any(s.get("SceneDescription") for s in segs)
