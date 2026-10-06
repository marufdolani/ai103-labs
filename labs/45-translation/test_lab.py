import pytest


def test_autodetect_and_multi_target(result):
    t = result["text"]
    assert t["detected"] == "de"
    assert set(t["translations"]) == {"en", "fr", "ja"}
    assert "June" in t["translations"]["en"]


def test_brand_kept_in_llm_translation(result):
    assert "Contoso" in result["llm"]["text"]
    assert any("぀" <= ch <= "ヿ" for ch in result["llm"]["text"]), "expected Japanese kana"


def test_document_translation_keeps_markup_and_glossary(result):
    if result.get("document_error"):
        pytest.skip(f"Document translation unavailable here: {result['document_error']}")
    doc = result["document_fr"]
    assert "<h1>" in doc and "Contoso Cloud" in doc
    assert "télétravail" in doc.lower()


def test_batch_succeeded(result):
    if result.get("batch_error"):
        pytest.skip(f"Batch document translation unavailable here: {result['batch_error']}")
    assert result["batch"] and all("succeeded" in b["status"].lower() for b in result["batch"])
