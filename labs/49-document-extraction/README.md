# Lab 49 · Document Intelligence vs Content Understanding

**Scenario.** Contoso Accounts Payable receives scanned supplier invoices. Finance needs exact totals and invoice numbers it can trust, the ticked payment-status checkbox, and a suggested follow-up. The AI assistant needs clean Markdown it can ground on.

**Exam objectives.** D5 › *Extract information by using multimodal pipelines that combine OCR, layout analysis and field extraction*; *produce clean, grounded representations for agents and RAG by using Content Understanding*; *implement analyzers that generate structured or Markdown outputs for downstream reasoning*.

**You will learn**
- **Document Intelligence**: deterministic OCR + layout. Prebuilt models (`prebuilt-invoice`, receipts, IDs, …) return typed fields with confidence. `prebuilt-layout` returns **Markdown**, tables and **selection marks** (checkboxes).
- **Content Understanding**: you define a field schema. **extract** pulls literal values, **classify** picks from fixed categories (here, which checkbox is ticked), **generate** infers free text. Enable `estimateFieldSourceAndConfidence` to get **grounding** (where on the page) and confidence.
- When to use which:

| Need | Choose |
|---|---|
| Standard documents, known fields, deterministic | Document Intelligence prebuilt |
| Fixed layout, a few labelled samples | DI **custom template** |
| Varied layouts across vendors | DI **custom neural** |
| Route mixed document types | DI **custom classifier** / composed model |
| Your own schema, inferred or classified fields, multimodal, grounded Markdown for RAG/agents | **Content Understanding** analyzer |

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `DocumentIntelligenceClient(endpoint, credential)` | Keyless. |
| 2 | `begin_analyze_document("prebuilt-invoice", ...)` | Zero-training typed fields. |
| 3 | `prebuilt-layout`, `output_content_format="markdown"` | Tables + checkbox states, LLM-ready text. |
| 4 | Content Understanding analyzer on `prebuilt-document` with extract/classify/generate + grounding | One schema for the whole AP workflow. |

## Run and test
```bash
./lab run 49 && ./lab validate 49      # one click: ./lab solve 49
```
Open `.out/lab49/invoice.png` to see the test document.

## Explore
- Add `features=["queryFields"]` with `query_fields=["PONumber"]` to DI to pull an extra field with no training.
- Send the Content Understanding Markdown into the lab 20 index as a new chunk and ask the agent from lab 33 about it.

## Exam reflexes
- Invoices/receipts/IDs with no training → **DI prebuilt**. Checkboxes → **selection marks**.
- Fixed layout → **custom template**; varied layouts → **custom neural**.
- Classify/generate fields, grounding, Markdown for RAG, multimodal input → **Content Understanding**.

## Clean up
`./lab clean 49` deletes the analyzer.
