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
    # >>> TODO 1: Paragraph-aware chunking: accumulate paragraphs up to `size` chars, carry `overlap` chars forward
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for p in paras:
        if current and len(current) + len(p) > size:
            chunks.append(current)
            current = current[-overlap:] + "\n\n" + p
        else:
            current = f"{current}\n\n{p}" if current else p
    if current:
        chunks.append(current)
    return chunks
    # <<<


def create_index() -> None:
    # >>> TODO 2: Index with key, searchable text, filterable group_ids, a 3072-dim HNSW vector field with an Azure OpenAI vectorizer, and a semantic config
    index = SearchIndex(
        name=INDEX,
        fields=[
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SimpleField(name="doc_id", type=SearchFieldDataType.String, filterable=True),
            SearchableField(name="title", type=SearchFieldDataType.String),
            SearchableField(name="chunk", type=SearchFieldDataType.String),
            SimpleField(name="group_ids", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
            SearchField(name="chunk_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=DIMS, vector_search_profile_name="hnsw-profile"),
        ],
        vector_search=VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
            profiles=[VectorSearchProfile(name="hnsw-profile", algorithm_configuration_name="hnsw", vectorizer_name="aoai")],
            vectorizers=[AzureOpenAIVectorizer(vectorizer_name="aoai", parameters=AzureOpenAIVectorizerParameters(
                resource_url=cfg("FOUNDRY_OPENAI_ENDPOINT").rstrip("/"), deployment_name=cfg("EMBEDDING_MODEL"),
                model_name="text-embedding-3-large"))],
        ),
        semantic_search=SemanticSearch(default_configuration_name="default", configurations=[SemanticConfiguration(
            name="default", prioritized_fields=SemanticPrioritizedFields(
                title_field=SemanticField(field_name="title"), content_fields=[SemanticField(field_name="chunk")]))]),
    )
    search_index_client().create_or_update_index(index)
    # <<<


def upload() -> int:
    records = []
    for doc in load_docs():
        pieces = chunk(doc.text)
        # >>> TODO 3: Embed "title + chunk" for each piece and build records matching the index fields
        vectors = embed([f"{doc.title}\n{p}" for p in pieces])
        for i, (piece, vector) in enumerate(zip(pieces, vectors)):
            records.append({"id": f"{doc.id}-{i}", "doc_id": doc.id, "title": doc.title, "chunk": piece,
                            "group_ids": doc.groups, "chunk_vector": vector})
        # <<<
    search_client(INDEX).upload_documents(records)
    time.sleep(3)
    return len(records)


def query(question: str, mode: str) -> list[str]:
    client = search_client(INDEX)
    # >>> TODO 4: keyword | vector | hybrid | semantic (hybrid + semantic ranker); return doc_ids of the top 3
    vq = [VectorizedQuery(vector=embed([question])[0], k_nearest_neighbors=10, fields="chunk_vector")]
    kwargs = {
        "keyword": {"search_text": question},
        "vector": {"search_text": None, "vector_queries": vq},
        "hybrid": {"search_text": question, "vector_queries": vq},
        "semantic": {"search_text": question, "vector_queries": vq, "query_type": "semantic",
                     "semantic_configuration_name": "default"},
    }[mode]
    return [r["doc_id"] for r in client.search(top=3, select=["doc_id"], **kwargs)]
    # <<<


def answer(question: str) -> str:
    hits = list(search_client(INDEX).search(search_text=question, top=3, query_type="semantic",
                                            semantic_configuration_name="default", select=["doc_id", "title", "chunk"]))
    context = "\n\n".join(f"[{h['doc_id']}] {h['title']}\n{h['chunk']}" for h in hits)
    # >>> TODO 5: Grounded generation: answer only from context and cite sources as [doc_id]
    resp = openai().responses.create(
        model=cfg("CHAT_MODEL"),
        instructions=("Answer using ONLY the sources. Cite each fact with its source id in square brackets, "
                      "e.g. [POL-HR-017]. If the sources don't contain the answer, say so."),
        input=f"SOURCES:\n{context}\n\nQUESTION: {question}",
        reasoning={"effort": "low"},
        max_output_tokens=2000,
    )
    return resp.output_text
    # <<<


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
