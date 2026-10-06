"""Lab 41 - Multimodal understanding: captions, grounded visual Q&A, objects, alt text."""
from pydantic import BaseModel

from labkit import cfg, show
from labkit.clients import openai
from labkit.images import bar_chart, store_shelf, to_data_url

CHART, SHELF = to_data_url(bar_chart()), to_data_url(store_shelf())


def image_part(url: str, detail: str = "high") -> dict:
    return {"type": "input_image", "image_url": url, "detail": detail}


def look(prompt: str, images: list[str], instructions: str = "", fmt=None, detail: str = "high"):
    content = [{"type": "input_text", "text": prompt}, *(image_part(u, detail) for u in images)]
    kwargs = dict(model=cfg("LARGE_MODEL"), instructions=instructions or None, reasoning={"effort": "low"},
                  input=[{"role": "user", "content": content}], max_output_tokens=3000)
    if fmt:
        return openai().responses.parse(text_format=fmt, **kwargs).output_parsed
    return openai().responses.create(**kwargs).output_text.strip()


class ShelfItem(BaseModel):
    kind: str
    color: str
    count: int
    approx_box: list[int]  # [x_min, y_min, x_max, y_max] in pixels for the group


class Shelf(BaseModel):
    items: list[ShelfItem]


GROUNDED = ("Answer ONLY from what is visible in the image(s). If the image does not show the answer, reply exactly: "
            "'Cannot determine from the image.'")


def main() -> dict:
    # TODO 1: Concise (one sentence, low detail) and detailed captions of the chart
    raise NotImplementedError("TODO 1: Concise (one sentence, low detail) and detailed captions of the chart  (see README step and solution/ if stuck)")
    # TODO 2: One request with BOTH images: caption each, numbered
    raise NotImplementedError("TODO 2: One request with BOTH images: caption each, numbered  (see README step and solution/ if stuck)")
    # TODO 3: Grounded visual Q&A, including a question the image can't answer
    raise NotImplementedError("TODO 3: Grounded visual Q&A, including a question the image can't answer  (see README step and solution/ if stuck)")
    # TODO 4: Identify objects/regions on the shelf as structured output (kind, colour, count, approximate box)
    raise NotImplementedError("TODO 4: Identify objects/regions on the shelf as structured output (kind, colour, count, approximate box)  (see README step and solution/ if stuck)")
    # TODO 5: Accessibility: alt text (<=125 chars, purpose not appearance) + extended description
    raise NotImplementedError("TODO 5: Accessibility: alt text (<=125 chars, purpose not appearance) + extended description  (see README step and solution/ if stuck)")
    counts = {f"{i.color.lower()}": i.count for i in shelf.items}
    show.text("Concise", concise)
    show.text("Detailed", detailed, 400)
    show.text("Two images", multi)
    show.kv({"VQA (answerable)": vqa_answerable, "VQA (not in image)": vqa_unanswerable, "shelf counts": counts,
             "alt text": alt, "alt length": len(alt)})
    return {"concise": concise, "detailed": detailed, "multi": multi, "vqa_answerable": vqa_answerable,
            "vqa_unanswerable": vqa_unanswerable, "shelf": shelf.model_dump(), "alt": alt, "extended": extended}


if __name__ == "__main__":
    show.result(main())
