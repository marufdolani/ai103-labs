"""Lab 48 - Ingestion with an indexer + skillset: OCR, merge, chunking, integrated vectorization, index projections,
indexer health monitoring, and keyword vs vector vs hybrid vs semantic retrieval. Uses the Search REST API (JSON you
will recognise from the docs and the exam)."""
import time

from PIL import Image, ImageDraw

from labkit import cfg, show
from labkit.clients import SEARCH_SCOPE, Rest, RestError, blob_service
from labkit.images import _font, to_bytes
from labkit.rag import POLICY_DIR

API = "api-version=2024-07-01"
NAME = "lab48"                      # index, data source, skillset and indexer share this prefix
CONTAINER, PREFIX = "search-docs", "lab48/"
CODE = "XJ-4471-B"


def scanned_bulletin() -> bytes:
    """A 'scanned' maintenance bulletin. Its text exists only as pixels, so only OCR can make it searchable."""
    img = Image.new("RGB", (1100, 500), "white")
    d = ImageDraw.Draw(img)
    lines = ["CONTOSO FIELD SERVICE BULLETIN 2026-11",
             f"Replacement valve part number {CODE} supersedes XJ-4470.",
             "Tighten the valve housing bolts to 42 Nm in a star pattern.",
             "Technicians must wear cut-resistant gloves during replacement."]
    for i, line in enumerate(lines):
        d.text((40, 60 + i * 90), line, fill="black", font=_font(30))
    return to_bytes(img, "PNG")


def upload_corpus() -> int:
    container = blob_service().get_container_client(CONTAINER)
    files = {f"{PREFIX}{p.name}": p.read_bytes() for p in sorted(POLICY_DIR.glob("*.md"))}
    files[f"{PREFIX}bulletin-2026-11.png"] = scanned_bulletin()
    for name, data in files.items():
        container.upload_blob(name, data, overwrite=True)
    return len(files)


def search_rest() -> Rest:
    return Rest(cfg("SEARCH_ENDPOINT"), SEARCH_SCOPE)


def index_body() -> dict:
    return {
        "name": f"{NAME}-index",
        "fields": [
            # Index projections need a string key with the keyword analyzer; the parent key is filterable.
            {"name": "chunk_id", "type": "Edm.String", "key": True, "searchable": True, "analyzer": "keyword"},
            {"name": "parent_id", "type": "Edm.String", "filterable": True},
            {"name": "title", "type": "Edm.String", "searchable": True},
            {"name": "chunk", "type": "Edm.String", "searchable": True},
            {"name": "chunk_vector", "type": "Collection(Edm.Single)", "searchable": True, "retrievable": False,
             "dimensions": 3072, "vectorSearchProfile": "hnsw-aoai"},
        ],
        "vectorSearch": {
            "algorithms": [{"name": "hnsw", "kind": "hnsw"}],
            "profiles": [{"name": "hnsw-aoai", "algorithm": "hnsw", "vectorizer": "aoai"}],
            "vectorizers": [{"name": "aoai", "kind": "azureOpenAI", "azureOpenAIParameters": {
                "resourceUri": cfg("FOUNDRY_OPENAI_ENDPOINT").rstrip("/"), "deploymentId": cfg("EMBEDDING_MODEL"),
                "modelName": "text-embedding-3-large"}}],
        },
        "semantic": {"defaultConfiguration": "default", "configurations": [{
            "name": "default",
            "prioritizedFields": {"titleField": {"fieldName": "title"},
                                  "prioritizedContentFields": [{"fieldName": "chunk"}]}}]},
    }


def data_source_body() -> dict:
    # TODO 1: Blob data source that authenticates with the search service's managed identity (ResourceId=..., no keys)
    raise NotImplementedError("TODO 1: Blob data source that authenticates with the search service's managed identity (ResourceId=..., no keys)  (see README step and solution/ if stuck)")


def skillset_body() -> dict:
    # TODO 2: Skillset: OCR on normalized images -> Merge into text -> Split into pages -> Azure OpenAI embeddings
    raise NotImplementedError("TODO 2: Skillset: OCR on normalized images -> Merge into text -> Split into pages -> Azure OpenAI embeddings  (see README step and solution/ if stuck)")
    # TODO 3: Index projections: one search document per chunk (parent skipped), mapped from the enrichment tree
    raise NotImplementedError("TODO 3: Index projections: one search document per chunk (parent skipped), mapped from the enrichment tree  (see README step and solution/ if stuck)")
    return {"name": f"{NAME}-skillset", "skills": skills, "indexProjections": projections}


def indexer_body() -> dict:
    # TODO 4: Indexer: extract content + metadata AND normalized images so the OCR skill has input
    raise NotImplementedError("TODO 4: Indexer: extract content + metadata AND normalized images so the OCR skill has input  (see README step and solution/ if stuck)")


def wait_for_indexer(rest: Rest, timeout: int = 600) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = rest.get(f"indexers/{NAME}-indexer/status?{API}").json()
        last = status.get("lastResult") or {}
        if last.get("status") in {"success", "transientFailure", "error"} and last.get("endTime"):
            return status
        time.sleep(5)
    raise TimeoutError("Indexer did not finish in time")


def health(rest: Rest, status: dict) -> dict:
    # TODO 5: Ingestion health: run status, items processed/failed, errors and warnings, index document count
    raise NotImplementedError("TODO 5: Ingestion health: run status, items processed/failed, errors and warnings, index document count  (see README step and solution/ if stuck)")


def query(rest: Rest, mode: str, text: str) -> dict:
    body: dict = {"select": "title,chunk", "top": 3}
    # TODO 6: Build the request for each mode: keyword | vector | hybrid | semantic (hybrid + semantic ranker)
    raise NotImplementedError("TODO 6: Build the request for each mode: keyword | vector | hybrid | semantic (hybrid + semantic ranker)  (see README step and solution/ if stuck)")
    hits = rest.post(f"indexes/{NAME}-index/docs/search?{API}", body).json()["value"]
    top = hits[0] if hits else {}
    return {"top_title": top.get("title"), "score": top.get("@search.score"),
            "reranker": top.get("@search.rerankerScore"), "titles": [h.get("title") for h in hits]}


def main() -> dict:
    rest = search_rest()
    show.step("Upload corpus (6 policies + 1 scanned bulletin image)")
    uploaded = upload_corpus()
    show.step("Create index, data source, skillset, indexer")
    cleanup(rest)
    rest.put(f"indexes/{NAME}-index?{API}", index_body())
    rest.put(f"datasources/{NAME}-ds?{API}", data_source_body())
    rest.put(f"skillsets/{NAME}-skillset?{API}", skillset_body())
    rest.put(f"indexers/{NAME}-indexer?{API}", indexer_body())   # creating an indexer runs it

    show.step("Wait for the indexer, then check ingestion health")
    report = health(rest, wait_for_indexer(rest))
    show.kv(report)
    time.sleep(3)

    show.title("Retrieval modes")
    questions = {"exact code": CODE, "paraphrase": "how much torque for the valve housing bolts?"}
    results = {q: {m: query(rest, m, text) for m in ("keyword", "vector", "hybrid", "semantic")}
               for q, text in questions.items()}
    for q, by_mode in results.items():
        show.table([[m, r["top_title"], r["score"], r["reranker"]] for m, r in by_mode.items()],
                   [f"{q}: mode", "top document", "score", "reranker (0-4)"])
    return {"uploaded": uploaded, "health": report, "results": results}


def cleanup(rest: Rest | None = None) -> None:
    rest = rest or search_rest()
    for path in (f"indexers/{NAME}-indexer", f"skillsets/{NAME}-skillset", f"datasources/{NAME}-ds", f"indexes/{NAME}-index"):
        try:
            rest.delete(f"{path}?{API}")
        except RestError:
            pass


if __name__ == "__main__":
    show.result(main())
