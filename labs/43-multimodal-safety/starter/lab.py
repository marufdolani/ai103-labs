"""Lab 43 - Responsible AI for images: moderation, injection via embedded text, watermark and brand policy."""
import base64

from PIL import Image, ImageDraw, PngImagePlugin
from pydantic import BaseModel

from labkit import cfg, out_path, show
from labkit.clients import Rest, openai
from labkit.images import _font, injected_screenshot, product_photo, to_bytes, to_data_url

IMAGE_ANALYZE = "contentsafety/image:analyze?api-version=2024-09-01"
SHIELD = "contentsafety/text:shieldPrompt?api-version=2024-09-01"


class BrandCheck(BaseModel):
    brand_logo_present: bool
    brand_logo_text: str
    prohibited_symbols: list[str]
    inappropriate_content: bool


def moderate(img: Image.Image) -> dict:
    # TODO 1: Content Safety image:analyze with base64 content; return {category: severity}
    raise NotImplementedError("TODO 1: Content Safety image:analyze with base64 content; return {category: severity}  (see README step and solution/ if stuck)")


def screenshot_guard(img: Image.Image) -> dict:
    # TODO 2: Transcribe the screenshot text, screen it with Prompt Shields as a DOCUMENT, then answer with spotlighting
    raise NotImplementedError("TODO 2: Transcribe the screenshot text, screen it with Prompt Shields as a DOCUMENT, then answer with spotlighting  (see README step and solution/ if stuck)")
    return {"transcript": transcript, "attack_detected": attack, "answer": answer}


def watermark(img: Image.Image) -> str:
    # TODO 3: Visible watermark + provenance metadata in the PNG (tEXt chunk)
    raise NotImplementedError("TODO 3: Visible watermark + provenance metadata in the PNG (tEXt chunk)  (see README step and solution/ if stuck)")


def brand_policy(img: Image.Image) -> BrandCheck:
    # TODO 4: Vision model returns a BrandCheck (logo present, prohibited symbols, inappropriate content)
    raise NotImplementedError("TODO 4: Vision model returns a BrandCheck (logo present, prohibited symbols, inappropriate content)  (see README step and solution/ if stuck)")


def main() -> dict:
    severities = moderate(product_photo())
    show.kv({"moderation (product photo)": severities})
    guard = screenshot_guard(injected_screenshot())
    show.kv({"injection detected in image text": guard["attack_detected"]})
    show.text("Assistant answer", guard["answer"])
    path = watermark(product_photo())
    stored = Image.open(path).text.get("provenance", "")
    brand = brand_policy(product_photo())
    show.kv({"watermarked file": path, "provenance metadata": stored, "brand check": brand.model_dump()})
    return {"severities": severities, "guard": guard, "provenance": stored, "brand": brand.model_dump()}


if __name__ == "__main__":
    show.result(main())
