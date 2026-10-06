# Lab 45 · Translate text and documents

**Scenario.** Contoso Cloud sends billing notices worldwide and must translate HR policies into French without breaking formatting. The brand name must never be translated, and Japanese customer notices must be in formal register.

**Exam objectives.** D4 › *Build solutions that translate text by using Azure Translator in Foundry Tools or LLM-powered translation flows*.

**You will learn**
- **Text translation**: several `to` languages in one call; leave `from` out to auto-detect.
- **LLM-powered translation**: Translator can target your own model deployment (`deployment_name`) with `tone` and `gender`. A Responses API prompt is the fallback, and both let you control register.
- **Single-document translation** (synchronous, no storage) vs **batch Document Translation** (asynchronous, Blob container to Blob container, many files and formats).
- **Glossaries** (TSV/CSV/XLF) keep terminology consistent. **Custom Translator** is the trained option when a glossary isn't enough.
- Keyless storage access: the Foundry resource's **managed identity** has Storage Blob Data Contributor, so no SAS tokens.

## Set up
The platform created the `translate-src` and `translate-out` containers and the role assignment.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `TextTranslationClient(endpoint, credential)` | Custom endpoint + Entra ID. |
| 2 | `translate(body=[text], to_language=["en","fr","ja"])` | One request, three languages, auto-detect. |
| 3 | `TranslationTarget(language="ja", deployment_name=..., tone="formal")` with fallback | LLM translation with controlled tone. |
| 4 | `SingleDocumentTranslationClient.translate(DocumentTranslateContent(document, glossary))` | Formatting preserved; brand kept. |
| 5 | `DocumentTranslationClient.begin_translation(src, out, "fr", prefix, glossaries)` | Batch, asynchronous, storage-based. |

## Run and test
```bash
./lab run 45 && ./lab validate 45      # one click: ./lab solve 45
```

## Explore
- Add `ProfanityAction` and `transliterate` (Japanese to Latin script).
- Put a `.docx` or `.pdf` in `translate-src` and rerun the batch. Then check `translate_text_within_image`.
- In the Speech lab (46) you'll translate *speech*. Compare the latency and cost.

## Exam reflexes
- Many languages in one call → repeat `to`; unknown source → omit `from`.
- Whole Word/PDF files with layout → **Document Translation**. One file now → **single-document**; many files → **batch with Blob containers**.
- Brand/terms must stay consistent → **glossary**; domain style learned from parallel data → **Custom Translator**.
- Register or tone control → **LLM translation** (Translator `deployment_name` + `tone`, or a prompt).

## Clean up
Translated files land in `translate-out/lab45/...`. Delete them in the portal or ignore them (they cost cents).
