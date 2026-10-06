# Lab 42 · Content Understanding for images and video

**Scenario.** Contoso's digital-asset library holds thousands of charts and product videos with no metadata. You need consistent, schema-based fields (chart type, title, insight, alt text; per-scene descriptions for video) that downstream search and agents can rely on.

**Exam objectives.** D3 › *Implement visual understanding by configuring Azure Content Understanding to extract visual characteristics*; *implement video analysis workflows to process and interpret video segments*; *configure single-task and pro-mode Content Understanding pipelines*. D5 › *Produce clean, grounded representations to use with agents and RAG*.

**You will learn**
- Content Understanding uses **your** model deployments: set resource defaults once (`PATCH /contentunderstanding/defaults`).
- **Prebuilt** analyzers (`prebuilt-imageSearch`, `prebuilt-videoSearch`, `prebuilt-invoice`, …) vs **custom** analyzers (base analyzer + field schema).
- Field methods: **extract** (literal values, documents only), **classify** (fixed categories), **generate** (free-form, inferred).
- Video results come back per **segment** with start/end times, markdown (key frames, transcript) and your fields.

## Set up
Uses Microsoft's public sample files (a pie chart and a short video). Video analysis takes a few minutes.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Map model aliases to your deployments. | Content Understanding bills tokens on your deployments. |
| 2 | Prebuilt image analysis → markdown. | Zero-config grounding text for RAG. |
| 3 | Custom image analyzer (classify + generate). | Your schema, consistent output. |
| 4 | Custom video analyzer, per-segment fields. | Scene-level metadata. |

## Run and test
```bash
./lab run 42 && ./lab validate 42      # one click: ./lab solve 42
./lab clean 42
```

## Explore
- Turn on `estimateFieldSourceAndConfidence` (documents) to get grounding regions and confidence per field.
- **Pro mode** (multi-file tasks with reference data, documents only) was a 2025 preview, and newer API versions offer **agentic mode** for cross-document reasoning. Know the concept: standard = single file, schema extraction; pro/agentic = reasoning across files plus reference data for validation.

## Exam reflexes
- Schema-based fields from images/audio/video/documents, with grounding → **Content Understanding custom analyzer**.
- Fixed list → **classify**; free text inferred → **generate**; literal text from a document → **extract**.
- Multi-document reasoning against reference data → **pro mode / agentic mode**.

## Clean up
`./lab clean 42`
