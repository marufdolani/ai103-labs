# Lab 44 · Text analysis: Language service vs LLM

**Scenario.** Contoso Hospitality receives reviews in many languages and support tickets full of personal data. Analytics needs aspect-level sentiment and entities. Compliance needs PII redacted before storage and memos reduced to obligations and deadlines. Trust & Safety needs threats flagged.

**Exam objectives.** D4 › *Extract entities, topics, summaries and structured JSON using generative prompting and Foundry Tools*; *detect sentiment, tone, safety issues and sensitive content*; *customise language model outputs for domain tasks such as compliance summarisation*.

**You will learn**
- Azure Language in Foundry Tools gives you **deterministic, scored** results: language detection, sentiment with **opinion mining**, NER, key phrases and **PII redaction**. All of it runs on the same Foundry resource, keyless.
- An LLM with **structured outputs** covers what the service doesn't score: tone, free-form topics, and domain-specific summaries.
- **Content Safety** text analysis returns a severity per harm category.

## Set up
Nothing extra. Uses your Foundry resource (Cognitive Services User role, assigned by the platform).

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `TextAnalyticsClient(endpoint, DefaultAzureCredential())` | Keyless; custom subdomain endpoint required for Entra ID. |
| 2 | Detect language → sentiment with `show_opinion_mining=True` → entities → key phrases | Aspect-level sentiment: *food* positive, *service* negative. |
| 3 | `recognize_pii_entities` → `redacted_text` | Auditable redaction with categories and confidence. |
| 4 | Same review via `responses.parse(text_format=ReviewInsight)` | Tone and topics with a guaranteed schema. |
| 5 | Compliance summary prompt with a strict schema | Domain customisation by instruction plus schema. |
| 6 | `contentsafety/text:analyze` | Harm severities (0/2/4/6). |

## Run and test
```bash
./lab run 44            # your starter
./lab validate 44       # tests against your code
./lab solve 44          # one click: reference solution + tests
```

## Explore
- Add `begin_analyze_healthcare_entities` (Text Analytics for health) on a clinical note and look at negation and relations.
- Use `begin_analyze_actions` to run several analyses in one async batch.
- Language also hosts **custom** models: custom text classification (single/multi-label), custom NER, CLU (intents and entities) and custom question answering. They need labelled data, so here you only need to know when to choose each.

## Exam reflexes
- PII redaction you can audit → **Language PII detection**, not a free-form LLM prompt.
- Sentiment *about specific aspects* → **opinion mining**.
- Tone, nuance or a custom JSON shape → **LLM + structured outputs**.
- Trained intents/entities from utterances → **CLU** (LUIS is retired). Curated FAQ answers → **custom question answering**.

## Clean up
Nothing is created.
