"""Shared retrieval helpers: the Contoso policy corpus and the `policies` search index.

Lab 20 has you build this yourself. Later labs (26, 33, 37, 50) call ensure_policy_index()
so they work even if you skipped lab 20.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .config import ROOT, cfg

POLICY_DIR = ROOT / "data" / "policies"
INDEX_NAME = "policies"
VECTOR_DIMS = 3072  # text-embedding-3-large native size; the integrated vectorizer embeds queries at this size


@dataclass
class Doc:
    id: str
    title: str
    text: str
    groups: list[str]
    source: str


def load_docs() -> list[Doc]:
    docs = []
    for path in sorted(POLICY_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta, body = raw.split("---", 2)[1:]
        fields = dict(line.split(":", 1) for line in meta.strip().splitlines())
        docs.append(Doc(
            id=fields["id"].strip(),
            title=fields["title"].strip(),
            text=body.strip(),
            groups=[g.strip() for g in fields["groups"].split(",")],
            source=path.name,
        ))
    return docs


def chunk(text: str, size: int = 700, overlap: int = 100) -> list[str]:
    """Paragraph-aware chunking with character overlap."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
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


def index_definition(name: str = INDEX_NAME):
    from azure.search.documents.indexes.models import (
        AzureOpenAIVectorizer, AzureOpenAIVectorizerParameters, HnswAlgorithmConfiguration,
        SearchableField, SearchField, SearchFieldDataType, SearchIndex, SemanticConfiguration,
        SemanticField, SemanticPrioritizedFields, SemanticSearch, SimpleField, VectorSearch,
        VectorSearchProfile,
    )

    return SearchIndex(
        name=name,
        fields=[
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SimpleField(name="doc_id", type=SearchFieldDataType.String, filterable=True),
            SearchableField(name="title", type=SearchFieldDataType.String),
            SearchableField(name="chunk", type=SearchFieldDataType.String),
            SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
            SimpleField(name="group_ids", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
            SearchField(
                name="chunk_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=VECTOR_DIMS,
                vector_search_profile_name="hnsw-profile",
            ),
        ],
        vector_search=VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
            profiles=[VectorSearchProfile(name="hnsw-profile", algorithm_configuration_name="hnsw", vectorizer_name="aoai")],
            vectorizers=[AzureOpenAIVectorizer(
                vectorizer_name="aoai",
                parameters=AzureOpenAIVectorizerParameters(
                    resource_url=cfg("FOUNDRY_OPENAI_ENDPOINT").rstrip("/"),
                    deployment_name=cfg("EMBEDDING_MODEL"),
                    model_name="text-embedding-3-large",
                ),
            )],
        ),
        semantic_search=SemanticSearch(
            default_configuration_name="default",
            configurations=[SemanticConfiguration(
                name="default",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="title"),
                    content_fields=[SemanticField(field_name="chunk")],
                ),
            )],
        ),
    )


def build_records(docs: list[Doc]) -> list[dict]:
    from .clients import embed

    records = []
    for doc in docs:
        pieces = chunk(doc.text)
        vectors = embed([f"{doc.title}\n{p}" for p in pieces])
        for i, (piece, vector) in enumerate(zip(pieces, vectors)):
            records.append({
                "id": f"{doc.id}-{i}".replace(".", "_"),
                "doc_id": doc.id,
                "title": doc.title,
                "chunk": piece,
                "source": doc.source,
                "group_ids": doc.groups,
                "chunk_vector": vector,
            })
    return records


def ensure_policy_index(name: str = INDEX_NAME) -> str:
    """Create and populate the policy index if it doesn't exist yet. Idempotent."""
    from .clients import search_client, search_index_client

    indexes = search_index_client()
    if name not in set(indexes.list_index_names()):
        indexes.create_or_update_index(index_definition(name))
    client = search_client(name)
    if client.get_document_count() == 0:
        client.upload_documents(build_records(load_docs()))
        import time
        time.sleep(3)  # let the index refresh
    return name


def hybrid_search(query: str, *, top: int = 4, group: str | None = None, name: str = INDEX_NAME) -> list[dict]:
    """Hybrid (keyword + vector) query with semantic reranking and optional security trimming."""
    from azure.search.documents.models import VectorizableTextQuery

    from .clients import search_client

    flt = f"group_ids/any(g: g eq '{group}')" if group else None
    results = search_client(name).search(
        search_text=query,
        vector_queries=[VectorizableTextQuery(text=query, k_nearest_neighbors=20, fields="chunk_vector")],
        query_type="semantic",
        semantic_configuration_name="default",
        filter=flt,
        top=top,
        select=["id", "doc_id", "title", "chunk", "source"],
    )
    return [dict(r) for r in results]


def format_context(hits: list[dict]) -> str:
    return "\n\n".join(f"[{h['doc_id']}] {h['title']}\n{h['chunk']}" for h in hits)
