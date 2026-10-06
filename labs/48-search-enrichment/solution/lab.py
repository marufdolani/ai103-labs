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
    # >>> TODO 1: Blob data source that authenticates with the search service's managed identity (ResourceId=..., no keys)
    return {"name": f"{NAME}-ds", "type": "azureblob",
            "credentials": {"connectionString": f"ResourceId={cfg('STORAGE_RESOURCE_ID')};"},
            "container": {"name": CONTAINER, "query": PREFIX.rstrip("/")}}
    # <<<


def skillset_body() -> dict:
    # >>> TODO 2: Skillset: OCR on normalized images -> Merge into text -> Split into pages -> Azure OpenAI embeddings
    skills = [
        {"@odata.type": "#Microsoft.Skills.Vision.OcrSkill", "name": "ocr", "context": "/document/normalized_images/*",
         "detectOrientation": True,
         "inputs": [{"name": "image", "source": "/document/normalized_images/*"}],
         "outputs": [{"name": "text", "targetName": "text"}]},
        {"@odata.type": "#Microsoft.Skills.Text.MergeSkill", "name": "merge", "context": "/document",
         "inputs": [{"name": "text", "source": "/document/content"},
                    {"name": "itemsToInsert", "source": "/document/normalized_images/*/text"},
                    {"name": "offsets", "source": "/document/normalized_images/*/contentOffset"}],
         "outputs": [{"name": "mergedText", "targetName": "merged_content"}]},
        {"@odata.type": "#Microsoft.Skills.Text.SplitSkill", "name": "split", "context": "/document",
         "textSplitMode": "pages", "maximumPageLength": 1200, "pageOverlapLength": 150,
         "inputs": [{"name": "text", "source": "/document/merged_content"}],
         "outputs": [{"name": "textItems", "targetName": "pages"}]},
        {"@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill", "name": "embed",
         "context": "/document/pages/*", "resourceUri": cfg("FOUNDRY_OPENAI_ENDPOINT").rstrip("/"),
         "deploymentId": cfg("EMBEDDING_MODEL"), "modelName": "text-embedding-3-large", "dimensions": 3072,
         "inputs": [{"name": "text", "source": "/document/pages/*"}],
         "outputs": [{"name": "embedding", "targetName": "vector"}]},
    ]
    # <<<
    # >>> TODO 3: Index projections: one search document per chunk (parent skipped), mapped from the enrichment tree
    projections = {"selectors": [{
        "targetIndexName": f"{NAME}-index", "parentKeyFieldName": "parent_id", "sourceContext": "/document/pages/*",
        "mappings": [{"name": "chunk", "source": "/document/pages/*"},
                     {"name": "chunk_vector", "source": "/document/pages/*/vector"},
                     {"name": "title", "source": "/document/metadata_storage_name"}]}],
        "parameters": {"projectionMode": "skipIndexingParentDocuments"}}
    # <<<
    return {"name": f"{NAME}-skillset", "skills": skills, "indexProjections": projections}


def indexer_body() -> dict:
    # >>> TODO 4: Indexer: extract content + metadata AND normalized images so the OCR skill has input
    return {"name": f"{NAME}-indexer", "dataSourceName": f"{NAME}-ds", "skillsetName": f"{NAME}-skillset",
            "targetIndexName": f"{NAME}-index",
            "parameters": {"maxFailedItems": 0, "configuration": {
                "dataToExtract": "contentAndMetadata", "imageAction": "generateNormalizedImages",
                "parsingMode": "default"}}}
    # <<<


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
    # >>> TODO 5: Ingestion health: run status, items processed/failed, errors and warnings, index document count
    last = status["lastResult"]
    stats = rest.get(f"indexes/{NAME}-index/stats?{API}").json()
    return {"status": last["status"], "processed": last.get("itemsProcessed"), "failed": last.get("itemsFailed"),
            "errors": [e.get("errorMessage", "")[:160] for e in last.get("errors", [])],
            "warnings": [w.get("message", "")[:160] for w in last.get("warnings", [])],
            "chunks_indexed": stats["documentCount"]}
    # <<<


def query(rest: Rest, mode: str, text: str) -> dict:
    body: dict = {"select": "title,chunk", "top": 3}
    # >>> TODO 6: Build the request for each mode: keyword | vector | hybrid | semantic (hybrid + semantic ranker)
    if mode in {"keyword", "hybrid", "semantic"}:
        body["search"] = text
    if mode in {"vector", "hybrid", "semantic"}:
        body["vectorQueries"] = [{"kind": "text", "text": text, "fields": "chunk_vector", "k": 10}]
    if mode == "semantic":
        body.update({"queryType": "semantic", "semanticConfiguration": "default", "captions": "extractive"})
    # <<<
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
