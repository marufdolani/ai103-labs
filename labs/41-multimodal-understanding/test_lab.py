def test_concise_shorter_than_detailed(result):
    assert len(result["concise"]) < len(result["detailed"])


def test_detailed_reads_values(result):
    for value in ("40", "55", "80", "65"):
        assert value in result["detailed"]


def test_multi_image_captions(result):
    text = result["multi"]
    assert "1" in text and "2" in text
    assert "chart" in text.lower() and ("shelf" in text.lower() or "product" in text.lower())


def test_grounded_vqa(result):
    assert "Q3" in result["vqa_answerable"] and "80" in result["vqa_answerable"]
    assert "cannot determine" in result["vqa_unanswerable"].lower()


def test_shelf_counts(result):
    counts = {}
    for item in result["shelf"]["items"]:
        counts[item["color"].lower()] = counts.get(item["color"].lower(), 0) + item["count"]
    assert counts.get("red") == 3 and counts.get("blue") == 2 and counts.get("green") == 1, counts


def test_alt_text_guidelines(result):
    alt = result["alt"]
    assert len(alt) <= 125 and not alt.lower().startswith(("image of", "picture of"))
    assert len(result["extended"]) > len(alt)
