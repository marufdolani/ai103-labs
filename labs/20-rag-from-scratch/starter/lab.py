"""Lab 20 - RAG from scratch with hybrid and semantic search."""
import time

from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizer, AzureOpenAIVectorizerParameters, HnswAlgorithmConfiguration, SearchableField, SearchField,
    SearchFieldDataType, SearchIndex, SemanticConfiguration, SemanticField, SemanticPrioritizedFields, SemanticSearch,
    SimpleField, VectorSearch, VectorSearchProfile,
)
from azure.search.documents.models import VectorizedQuery

from labkit import cfg, show
from labkit.clients import embed, openai, search_client, search_index_client
from labkit.rag import load_docs

INDEX = "lab20-policies"
DIMS = 3072
QUESTIONS = {
    "What is policy POL-IT-009 about?": "POL-IT-009",          # exact identifier: keyword shines
    "Can I fly business class to Tokyo for a client visit?": "POL-FIN-004",
    "How long can new parents take off work?": "POL-HR-017",   # paraphrase: vectors shine
}


def chunk(text: str, size: int = 700, overlap: int = 100) -> list[str]:
    # TODO 1: Paragraph-aware chunking: accumulate paragraphs up to `size` chars, carry `overlap` chars forward
    raise NotImplementedError("TODO 1: Paragraph-aware chunking: accumulate paragraphs up to `size` chars, carry `overlap` chars forward  (see README step and solution/ if stuck)")


def create_index() -> None:
    # TODO 2: Index with key, searchable text, filterable group_ids, a 3072-dim HNSW vector field with an Azure OpenAI vectorizer, and a semantic config
    raise NotImplementedError("TODO 2: Index with key, searchable text, filterable group_ids, a 3072-dim HNSW vector field with an Azure OpenAI vectorizer, and a semantic config  (see README step and solution/ if stuck)")


def upload() -> int:
    records = []
    for doc in load_docs():
        pieces = chunk(doc.text)
        # TODO 3: Embed "title + chunk" for each piece and build records matching the index fields
        raise NotImplementedError("TODO 3: Embed 'title + chunk' for each piece and build records matching the index fields  (see README step and solution/ if stuck)")
    search_client(INDEX).upload_documents(records)
    time.sleep(3)
    return len(records)


def query(question: str, mode: str) -> list[str]:
    client = search_client(INDEX)
    # TODO 4: keyword | vector | hybrid | semantic (hybrid + semantic ranker); return doc_ids of the top 3
    raise NotImplementedError("TODO 4: keyword | vector | hybrid | semantic (hybrid + semantic ranker); return doc_ids of the top 3  (see README step and solution/ if stuck)")


def answer(question: str) -> str:
    hits = list(search_client(INDEX).search(search_text=question, top=3, query_type="semantic",
                                            semantic_configuration_name="default", select=["doc_id", "title", "chunk"]))
    context = "\n\n".join(f"[{h['doc_id']}] {h['title']}\n{h['chunk']}" for h in hits)
    # TODO 5: Grounded generation: answer only from context and cite sources as [doc_id]
    raise NotImplementedError("TODO 5: Grounded generation: answer only from context and cite sources as [doc_id]  (see README step and solution/ if stuck)")


def main() -> dict:
    show.step("Create index and upload chunks")
    create_index()
    count = upload()
    show.ok(f"{count} chunks indexed in '{INDEX}'")

    modes = ["keyword", "vector", "hybrid", "semantic"]
    top1 = {q: {m: (query(q, m) or ["-"])[0] for m in modes} for q in QUESTIONS}
    show.title("Top-1 document per retrieval mode")
    show.table([[q[:45], expected, *(("✓ " if top1[q][m] == expected else "✗ ") + top1[q][m] for m in modes)]
                for q, expected in QUESTIONS.items()], ["question", "expected", *modes])

    q = "How long can new parents take off work, and when do I need to apply?"
    grounded = answer(q)
    show.text("Grounded answer", grounded)
    return {"chunks": count, "top1": top1, "expected": QUESTIONS, "answer": grounded}


def cleanup() -> None:
    search_index_client().delete_index(INDEX)


if __name__ == "__main__":
    show.result(main())
