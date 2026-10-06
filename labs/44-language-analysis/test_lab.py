def test_language_detection(result):
    assert result["language"]["languages"] == ["en", "fr", "ja"]


def test_opinion_mining_finds_negative_service(result):
    ops = {o["target"].lower(): o["sentiment"] for o in result["language"]["opinions"]}
    assert ops.get("service") == "negative", ops
    assert ops.get("food") == "positive", ops


def test_entities(result):
    cats = {e["category"] for e in result["language"]["entities"]}
    assert "Location" in cats or "Organization" in cats


def test_pii_redacted(result):
    red = result["language"]["redacted"]
    assert "555-0134" not in red and "maria.garcia@example.com" not in red
    assert "PhoneNumber" in result["language"]["pii_categories"]


def test_llm_structured(result):
    review = result["llm"]["review"]
    assert review["language"] == "en" and review["complaint_topics"]
    comp = result["llm"]["compliance"]
    assert any("72" in o for o in comp["obligations"]) or any("72" in d for d in comp["deadlines"])
    assert not any("party" in o.lower() or "parking" in o.lower() for o in comp["obligations"])


def test_safety_flags_violence(result):
    assert result["safety"]["Violence"] >= 2
