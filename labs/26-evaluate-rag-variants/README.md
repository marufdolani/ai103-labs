# Lab 26 · Evaluate and compare app variants

**Scenario.** Two engineers disagree: "keyword search with one result is enough" vs "hybrid + semantic with four results". You'll settle it with data: run both variants over the same questions and compare **retrieval quality**, **groundedness** and **completeness** against ground truth.

**Exam objectives.** D2 › *Evaluate models and apps, including detecting fabrications, relevance, quality*. D1 › *Monitor … grounding quality*; *monitor … relevance performance*. D5 › *Configure semantic, hybrid and vector search for grounding*.

**You will learn**
- RAG evaluators: **Retrieval** (were the right chunks retrieved?), **Groundedness** (is the answer supported?), **Response Completeness** (does it cover the ground truth?).
- Why separating retrieval quality from generation quality tells you *where* to fix a RAG app.

## Set up
Uses the shared `policies` index (created automatically by `labkit.rag.ensure_policy_index()`).

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Variant A retriever: keyword, top 1. | The cheap baseline. |
| 2 | Variant B retriever: hybrid + semantic, top 4. | The candidate. |
| 3 | Score each answer with three evaluators. | Retrieval vs generation diagnostics. |

## Run and test
```bash
./lab run 26 && ./lab validate 26      # one click: ./lab solve 26
```

## Explore
- Make variant C: hybrid without semantic ranker. Where does the gain come from?
- Lower groundedness with high retrieval → fix the *prompt*. Low retrieval → fix *chunking/indexing/query*.

## Exam reflexes
- Retrieved the wrong content → **Retrieval / Document Retrieval** evaluators. Answer not supported → **Groundedness**. Missing facts vs reference → **Response Completeness**.
- Ship decisions come from **side-by-side evaluation on the same dataset**.

## Clean up
Nothing to clean (the shared index is reused by later labs).
