from pathlib import Path


def test_three_images_saved(result):
    assert all(Path(p).stat().st_size > 10_000 for p in result["files"])


def test_requested_size(result):
    assert tuple(result["size"]) == (1024, 1024)


def test_mask_confined_the_edit(result):
    d = result["diffs"]
    assert d["masked_top"] > d["unmasked_bottom"], d
