# Lab 41 · Captions, visual Q&A and alt text

**Scenario.** Contoso's investor-relations site publishes charts and product photos. You need captions at two lengths, answers to questions grounded in what the image shows (and an honest "can't tell" otherwise), object counts for a retail-shelf audit, and accessible alt text.

**Exam objectives.** D3 › *Analyze visual context by using multimodal models*; *produce concise or detailed captions for single or multiple images*; *question-answering grounded in visual evidence*; *alt text and extended descriptions aligned to accessibility guidelines*; *identify objects, components, or regions within images*.

**You will learn**
- Image input parts: `{"type": "input_image", "image_url": <URL or data URL>, "detail": "low|high|auto"}`; several images per message.
- Grounding instructions for visual Q&A ("only from what's visible", fixed refusal text).
- Structured outputs over images (counts, colours, approximate regions).
- Alt text: short, purpose-first, no "image of"; extended descriptions carry the full data.

## Set up
Images are generated locally (`labkit/images.py`): a bar chart and a store shelf. No downloads.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Concise (low detail) vs detailed captions. | `detail: low` is cheaper; use it when fine detail doesn't matter. |
| 2 | Two images, one request. | Comparison and batch captioning. |
| 3 | Grounded Q&A incl. an unanswerable question. | Visual hallucination control. |
| 4 | Objects/regions as structured output. | Feeds downstream systems (inventory, QA). |
| 5 | Alt text + extended description. | WCAG-aligned accessibility. |

## Run and test
```bash
./lab run 41 && ./lab validate 41      # one click: ./lab solve 41
```

## Explore
- Ask for exact pixel bounding boxes and compare with the shapes in `store_shelf()`. LLM boxes are approximate. For precise detection use a dedicated model or Content Understanding (lab 42).

## Exam reflexes
- Describe / answer questions about images → **multimodal model with image input**. Precise, repeatable field extraction from images/video → **Content Understanding**.
- Alt text: concise, purpose-driven. Complex visuals → **extended description**.

## Clean up
Nothing to clean.
