# Lab 20 · RAG from scratch with hybrid and semantic search

**Scenario.** Employees ask the HR assistant about Contoso policies (`data/policies/*.md`). Answers must come only from current policy text, with citations. You'll build the whole pipeline: chunk → embed → index → retrieve (four ways) → generate with citations.

**Exam objectives.** D2 › *Implement RAG in an application*. D1 › *Choose an appropriate method for retrieval and indexing*. D5 › *Configure semantic search, hybrid search, and vector search for grounding*.

**You will learn**
- Index design: key, searchable, filterable (security trimming later), vector field (dimensions + HNSW profile), **vectorizer**, semantic configuration.
- Keyword (BM25) vs vector vs **hybrid (RRF fusion)** vs **hybrid + semantic ranker**, and when each wins.
- Grounding prompts that force citations and "I don't know".

## Set up
Nothing extra. The index `lab20-policies` is created in your Search service (Basic tier, semantic ranker free plan).

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Paragraph-aware chunking with overlap. | Chunks must be small enough to retrieve precisely and big enough to answer. |
| 2 | Create the index (fields, HNSW, vectorizer, semantic config). | The schema decides which queries are possible. |
| 3 | Embed and upload chunk records. | Vectors for semantic similarity; text for BM25. |
| 4 | Four retrieval modes, top-3 doc IDs. | See the difference on exact IDs vs paraphrases. |
| 5 | Grounded generation with `[doc_id]` citations. | The "G" in RAG, done responsibly. |

## Run and test
```bash
./lab run 20 && ./lab validate 20      # one click: ./lab solve 20
./lab clean 20                         # deletes the index
```

## Explore
- Add `filter="group_ids/any(g: g eq 'hr')"` to see **security trimming** (the bonus policy is HR-only).
- Add a scoring profile that boosts `title` matches.
- Because the index has a vectorizer, `VectorizableTextQuery(text=...)` lets Search embed the query for you.

## Exam reflexes
- Best general relevance → **hybrid + semantic ranker**. Exact codes or IDs → **keyword/hybrid** (vector-only misses them). Paraphrases → **vector/hybrid**.
- Semantic ranker needs a **semantic configuration**; it reranks the top results (L2) and can return captions/answers.
- Fresh knowledge → RAG, not fine-tuning.

## Clean up
`./lab clean 20`
