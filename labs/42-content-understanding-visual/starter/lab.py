"""Lab 42 - Content Understanding for images and video."""
from labkit import show
from labkit.cu import SAMPLES, analyze_url, create_analyzer, delete_analyzer, field_value, set_defaults

CHART_URL = f"{SAMPLES}/pieChart.jpg"
VIDEO_URL = f"{SAMPLES}/FlightSimulator.mp4"
IMAGE_ANALYZER, VIDEO_ANALYZER = "lab42_chart", "lab42_video"


def main() -> dict:
    show.step("0. Connect Content Understanding to your model deployments")
    # TODO 1: Set resource-level default model deployments (PATCH /contentunderstanding/defaults)
    raise NotImplementedError("TODO 1: Set resource-level default model deployments (PATCH /contentunderstanding/defaults)  (see README step and solution/ if stuck)")

    show.step("1. Prebuilt image analyzer")
    # TODO 2: Analyze the chart with prebuilt-imageSearch and keep the markdown
    raise NotImplementedError("TODO 2: Analyze the chart with prebuilt-imageSearch and keep the markdown  (see README step and solution/ if stuck)")
    show.text("Markdown", prebuilt_md, 400)

    show.step("2. Custom image analyzer: classify + generate fields")
    # TODO 3: Custom analyzer on prebuilt-image with a classify field (chart type) and generate fields (title, insight, alt text)
    raise NotImplementedError("TODO 3: Custom analyzer on prebuilt-image with a classify field (chart type) and generate fields (title, insight, alt text)  (see README step and solution/ if stuck)")
    show.kv(image_fields)

    show.step("3. Custom video analyzer: per-segment fields (takes a few minutes)")
    # TODO 4: Custom analyzer on prebuilt-video with per-segment generate/classify fields; analyze the sample video
    raise NotImplementedError("TODO 4: Custom analyzer on prebuilt-video with per-segment generate/classify fields; analyze the sample video  (see README step and solution/ if stuck)")
    show.table([[s["start_ms"], s["end_ms"], s.get("Setting"), str(s.get("SceneDescription"))[:60]] for s in segments],
               ["start ms", "end ms", "setting", "description"])
    return {"prebuilt_markdown": prebuilt_md, "image_fields": image_fields, "segments": segments}


def cleanup() -> None:
    delete_analyzer(IMAGE_ANALYZER)
    delete_analyzer(VIDEO_ANALYZER)


if __name__ == "__main__":
    show.result(main())
