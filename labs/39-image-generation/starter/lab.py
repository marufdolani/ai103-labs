"""Lab 39 - Generate and edit images: text-to-image, reference images, mask-based inpainting."""
import base64
import io

from PIL import Image, ImageChops, ImageDraw, ImageStat

from labkit import cfg, out_path, show
from labkit.clients import aoai

SIZE = (1024, 1024)


def save(b64: str, name: str):
    path = out_path("lab39", name)
    path.write_bytes(base64.b64decode(b64))
    return path


def make_mask(path) -> None:
    """Transparent pixels = area the model may change. Here: the top half (the background/wall)."""
    mask = Image.new("RGBA", SIZE, (0, 0, 0, 255))
    ImageDraw.Draw(mask).rectangle([0, 0, SIZE[0], SIZE[1] // 2], fill=(0, 0, 0, 0))
    mask.save(path)


def region_diff(a, b, box) -> float:
    da = Image.open(a).convert("RGB").resize(SIZE).crop(box)
    db = Image.open(b).convert("RGB").resize(SIZE).crop(box)
    return sum(ImageStat.Stat(ImageChops.difference(da, db)).mean) / 3


def main() -> dict:
    model = cfg("IMAGE_MODEL")
    show.step("1. Text to image")
    # TODO 1: Generate a 1024x1024 product photo (quality 'medium') and save it
    raise NotImplementedError("TODO 1: Generate a 1024x1024 product photo (quality 'medium') and save it  (see README step and solution/ if stuck)")

    show.step("2. Mask-based edit (inpainting): change only the wall")
    mask_path = out_path("lab39", "mask.png")
    make_mask(mask_path)
    # TODO 2: images.edit with image + mask + prompt; save the result
    raise NotImplementedError("TODO 2: images.edit with image + mask + prompt; save the result  (see README step and solution/ if stuck)")

    show.step("3. Prompt-driven modification from a reference image (no mask)")
    # TODO 3: images.edit with the original as a reference image to restyle the product
    raise NotImplementedError("TODO 3: images.edit with the original as a reference image to restyle the product  (see README step and solution/ if stuck)")

    top, bottom = (0, 0, SIZE[0], SIZE[1] // 2), (0, SIZE[1] // 2 + 40, SIZE[0], SIZE[1])
    diffs = {"masked_top": round(region_diff(original, edited, top), 1),
             "unmasked_bottom": round(region_diff(original, edited, bottom), 1)}
    raw = original.read_bytes()
    provenance = any(marker in raw for marker in (b"c2pa", b"jumb", b"C2PA"))
    show.kv({"files": [str(original), str(edited), str(restyled)], "pixel change": diffs,
             "C2PA content-credential marker found": provenance})
    return {"files": [str(p) for p in (original, edited, restyled)], "diffs": diffs, "c2pa_marker": provenance,
            "size": Image.open(io.BytesIO(raw)).size}


if __name__ == "__main__":
    show.result(main())
