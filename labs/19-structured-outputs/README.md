# Lab 19 · Structured outputs for downstream systems

**Scenario.** Contoso's finance system ingests invoices emailed as text, and the support team wants ticket insights (sentiment, tone, entities, topics, escalation flag) pushed to the CRM. Both integrations broke last month when the model "almost" returned the right JSON. You'll make the output schema-exact.

**Exam objectives.** D2 › *Integrate generative workflows into applications*. D4 › *Extract entities, topics, summaries, and structured JSON outputs by using generative prompting*; *configure detection of sentiment, tone*.

**You will learn**
- `responses.parse(text_format=PydanticModel)` → typed `output_parsed`.
- Raw `json_schema` with `strict: true` + `additionalProperties: false` + every property `required`.
- JSON mode (`json_object`) guarantees valid JSON only, not your fields.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Parse the invoice into the `Invoice` Pydantic model. | Typed objects, validated on arrival. |
| 2 | Ticket insights with a strict JSON schema (enums for sentiment and entity category). | Language-agnostic contract for other systems. |
| 3 | JSON mode for contrast. | Know why it's the weaker option. |

## Run and test
```bash
./lab run 19 && ./lab validate 19      # one click: ./lab solve 19
```

## Explore
- Remove `"escalate"` from `required` and see the API reject the schema in strict mode.
- Validate business rules *after* parsing (total = Σ qty × price). Schema ≠ correctness.

## Exam reflexes
- "Output must match a JSON schema" → **structured outputs, strict**. "Valid JSON is enough" → JSON mode.
- Generative extraction (flexible, zero-shot) vs **Azure Language** (deterministic, scored, PII categories). Compare in lab 44.

## Clean up
Nothing to clean.
