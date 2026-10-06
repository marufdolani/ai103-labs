# Lab 48 · Ingestion with skillsets and integrated vectorization

**Scenario.** Contoso Field Service has policies in Markdown and maintenance bulletins that exist only as **scanned images**. Technicians search by exact part numbers *and* by plain questions. Ops wants to know when ingestion breaks.

**Exam objectives.** D5 › *Ingest and index content such as documents and images*; *configure semantic, hybrid and vector search*; *implement enrichment with built-in skills for text, images and layout*; *configure RAG ingestion including OCR*. D1 › *Monitor data ingestion quality, search index health and relevance performance*.

**You will learn**
- The indexer pipeline: **data source** (Blob, managed identity) → **indexer** (`imageAction: generateNormalizedImages`) → **skillset** → **index**.
- Built-in skills: **OCR** → **Merge** (puts OCR text back in reading order) → **Split** (chunks) → **Azure OpenAI Embedding** (integrated vectorization).
- **Index projections**: one search document per chunk, with `parent_id` back to the source file.
- A **vectorizer** on the index embeds query text at search time, so the app sends text, not vectors.
- Health signals: indexer `lastResult` (status, items processed/failed, errors, warnings) and index stats.
- Retrieval modes side by side: **keyword** (BM25), **vector**, **hybrid** (RRF fusion) and **semantic** reranking (`@search.rerankerScore`, 0–4).

## Set up
The platform already gives the search service's identity *Storage Blob Data Reader* and *Cognitive Services OpenAI User*. With no billable AI services account attached, built-in OCR is free for 20 documents per indexer per day, which is plenty here.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Data source with `ResourceId=...;` connection string | Keyless: search's managed identity reads Blob. |
| 2 | Skills: OCR → Merge → Split → AzureOpenAIEmbedding | Make pixels searchable, chunk, vectorise. |
| 3 | `indexProjections` with `skipIndexingParentDocuments` | One-to-many: chunks become documents. |
| 4 | Indexer config `generateNormalizedImages` | Without it, OCR gets no input. |
| 5 | Status + stats → health report | What you'd alert on in production. |
| 6 | Query in four modes | See why hybrid + semantic is the default answer. |

## Run and test
```bash
./lab run 48 && ./lab validate 48      # one click: ./lab solve 48
./lab clean 48
```

## Explore
- Break it: set `imageAction` to `none`, rerun and watch the bulletin disappear from keyword results.
- Swap OCR + Merge for the **Document Layout skill** (Document Intelligence layout → Markdown with heading-aware chunks) on PDFs.
- Add a **knowledge store** (`knowledgeStore.projections`) to keep enriched output in tables/blobs for analytics.
- Turn on **incremental enrichment** (`cache`) so edits re-run only the affected skills.
- Use **Debug sessions** in the portal to step through the enrichment tree for one document.

## Exam reflexes
- Scanned PDFs/images → `generateNormalizedImages` + **OCR** (+ **Merge**), or **Document Layout**.
- Chunk and embed in the pipeline, text queries at runtime → **integrated vectorization** (Split + Embedding skill + **vectorizer**).
- Exact codes → keyword/hybrid. Meaning → vector. Best overall → **hybrid + semantic ranker**.
- Custom enrichment logic → **Custom Web API skill**. Enrichments for analytics → **knowledge store**.
- Indexer silently skipping docs → **indexer status / execution history** and **Debug sessions**.

## Clean up
`./lab clean 48` deletes the indexer, skillset, data source and index.
