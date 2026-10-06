BULLETIN = "bulletin-2026-11.png"


def test_indexer_healthy(result):
    h = result["health"]
    assert h["status"] == "success" and not h["failed"], h
    assert h["chunks_indexed"] >= result["uploaded"], "expected at least one chunk per document"


def test_ocr_made_image_searchable(result):
    assert result["results"]["exact code"]["keyword"]["top_title"] == BULLETIN


def test_hybrid_finds_exact_code(result):
    assert result["results"]["exact code"]["hybrid"]["top_title"] == BULLETIN


def test_semantic_reranks_paraphrase(result):
    sem = result["results"]["paraphrase"]["semantic"]
    assert sem["top_title"] == BULLETIN and sem["reranker"] is not None
