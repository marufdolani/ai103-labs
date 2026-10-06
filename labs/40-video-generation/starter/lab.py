"""Lab 40 - Generate and remix video with Sora (async jobs)."""
from PIL import Image, ImageDraw

from labkit import cfg, out_path, show
from labkit.clients import aoai


def save_video(video_id: str, name: str):
    content = aoai().videos.download_content(video_id, variant="video")
    path = out_path("lab40", name)
    path.write_bytes(content.read())
    return path


def reference_frame():
    """A simple first frame for image-to-video: a 1280x720 storefront sign."""
    path = out_path("lab40", "reference.png")
    img = Image.new("RGB", (1280, 720), (24, 64, 120))
    ImageDraw.Draw(img).rectangle([340, 260, 940, 460], fill=(245, 245, 240))
    ImageDraw.Draw(img).text((560, 345), "CONTOSO COFFEE", fill=(24, 64, 120))
    img.save(path)
    return path


def main() -> dict:
    model = cfg("VIDEO_MODEL")
    show.step("1. Text to video (async job; usually 1-3 minutes)")
    # TODO 1: create_and_poll a 4-second 1280x720 video from a prompt; download it
    raise NotImplementedError("TODO 1: create_and_poll a 4-second 1280x720 video from a prompt; download it  (see README step and solution/ if stuck)")
    show.kv({"id": v1.id, "status": v1.status, "file": first})

    show.step("2. Image to video (reference frame)")
    # TODO 2: Same, but pass input_reference=<reference image> so the video starts from it
    raise NotImplementedError("TODO 2: Same, but pass input_reference=<reference image> so the video starts from it  (see README step and solution/ if stuck)")
    show.kv({"id": v2.id, "status": v2.status, "file": second})

    show.step("3. Remix (edit) the first video with a new prompt")
    # TODO 3: videos.remix(v1.id, prompt=...) then poll until done; download
    raise NotImplementedError("TODO 3: videos.remix(v1.id, prompt=...) then poll until done; download  (see README step and solution/ if stuck)")
    show.kv({"id": remix.id, "status": remix.status, "file": third})
    return {"statuses": [v1.status, v2.status, remix.status], "files": [str(p) if p else None for p in (first, second, third)]}


if __name__ == "__main__":
    show.result(main())
