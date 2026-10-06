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
    # >>> TODO 1: Generate a 1024x1024 product photo (quality 'medium') and save it
    gen = aoai().images.generate(model=model, size="1024x1024", quality="medium", n=1,
                                 prompt=("Studio product photo of a white ceramic coffee mug with a small blue Contoso "
                                         "logo, on a light oak table, plain grey wall behind, soft daylight"))
    original = save(gen.data[0].b64_json, "mug.png")
    # <<<

    show.step("2. Mask-based edit (inpainting): change only the wall")
    mask_path = out_path("lab39", "mask.png")
    make_mask(mask_path)
    # >>> TODO 2: images.edit with image + mask + prompt; save the result
    with open(original, "rb") as img, open(mask_path, "rb") as mask:
        edit = aoai().images.edit(model=model, image=img, mask=mask, size="1024x1024",
                                  prompt="Replace the grey wall with a bright, sunny cafe window. Keep everything else.")
    edited = save(edit.data[0].b64_json, "mug_cafe.png")
    # <<<

    show.step("3. Prompt-driven modification from a reference image (no mask)")
    # >>> TODO 3: images.edit with the original as a reference image to restyle the product
    with open(original, "rb") as img:
        variant = aoai().images.edit(model=model, image=[img], size="1024x1024",
                                     prompt="Same mug and composition, but the mug is matte black with a white logo.")
    restyled = save(variant.data[0].b64_json, "mug_black.png")
    # <<<

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
