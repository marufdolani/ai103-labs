"""Lab 42 - Content Understanding for images and video."""
from labkit import show
from labkit.cu import SAMPLES, analyze_url, create_analyzer, delete_analyzer, field_value, set_defaults

CHART_URL = f"{SAMPLES}/pieChart.jpg"
VIDEO_URL = f"{SAMPLES}/FlightSimulator.mp4"
IMAGE_ANALYZER, VIDEO_ANALYZER = "lab42_chart", "lab42_video"


def main() -> dict:
    show.step("0. Connect Content Understanding to your model deployments")
    # >>> TODO 1: Set resource-level default model deployments (PATCH /contentunderstanding/defaults)
    set_defaults()
    # <<<

    show.step("1. Prebuilt image analyzer")
    # >>> TODO 2: Analyze the chart with prebuilt-imageSearch and keep the markdown
    prebuilt = analyze_url("prebuilt-imageSearch", CHART_URL)
    prebuilt_md = prebuilt["contents"][0].get("markdown", "")
    # <<<
    show.text("Markdown", prebuilt_md, 400)

    show.step("2. Custom image analyzer: classify + generate fields")
    # >>> TODO 3: Custom analyzer on prebuilt-image with a classify field (chart type) and generate fields (title, insight, alt text)
    create_analyzer(IMAGE_ANALYZER, {
        "description": "Chart analyzer for the investor-relations site",
        "baseAnalyzerId": "prebuilt-image",
        "models": {"completion": "prebuilt-analyzer-completion"},
        "fieldSchema": {"fields": {
            "ChartType": {"type": "string", "method": "classify", "enum": ["bar", "line", "pie", "scatter", "table", "other"],
                          "description": "Kind of chart"},
            "Title": {"type": "string", "method": "generate", "description": "Chart title or a short inferred title"},
            "KeyInsight": {"type": "string", "method": "generate", "description": "The single most important takeaway"},
            "AltText": {"type": "string", "method": "generate", "description": "Accessible alt text under 125 characters"},
        }},
    })
    custom = analyze_url(IMAGE_ANALYZER, CHART_URL)
    image_fields = {k: field_value(v) for k, v in custom["contents"][0].get("fields", {}).items()}
    # <<<
    show.kv(image_fields)

    show.step("3. Custom video analyzer: per-segment fields (takes a few minutes)")
    # >>> TODO 4: Custom analyzer on prebuilt-video with per-segment generate/classify fields; analyze the sample video
    create_analyzer(VIDEO_ANALYZER, {
        "description": "Segment-level scene analysis",
        "baseAnalyzerId": "prebuilt-video",
        "models": {"completion": "prebuilt-analyzer-completion"},
        "fieldSchema": {"fields": {
            "SceneDescription": {"type": "string", "method": "generate", "description": "What happens in this segment"},
            "Setting": {"type": "string", "method": "classify", "enum": ["cockpit", "outdoor aerial", "menu screen", "other"],
                        "description": "Where the segment takes place"},
        }},
    })
    video = analyze_url(VIDEO_ANALYZER, VIDEO_URL)
    segments = [{"start_ms": c.get("startTimeMs"), "end_ms": c.get("endTimeMs"),
                 **{k: field_value(v) for k, v in c.get("fields", {}).items()}} for c in video["contents"]]
    # <<<
    show.table([[s["start_ms"], s["end_ms"], s.get("Setting"), str(s.get("SceneDescription"))[:60]] for s in segments],
               ["start ms", "end ms", "setting", "description"])
    return {"prebuilt_markdown": prebuilt_md, "image_fields": image_fields, "segments": segments}


def cleanup() -> None:
    delete_analyzer(IMAGE_ANALYZER)
    delete_analyzer(VIDEO_ANALYZER)


if __name__ == "__main__":
    show.result(main())
