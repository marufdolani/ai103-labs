# Lab 18 · Prompt engineering and generation parameters

**Scenario.** Contoso's ticket triage uses a cheap small model, but priority labels are inconsistent, some answers are cut off, and the team keeps tweaking `temperature` with no effect. You'll fix the prompt with definitions and few-shot examples, diagnose truncation, control length with verbosity, and learn which sampling parameters apply to which models.

**Exam objectives.** D2 › *Tune generation behaviour, such as prompt engineering and adjusting model parameters*.

**You will learn**
- System instructions, delimiters (`"""…"""`), label definitions and few-shot examples.
- `max_output_tokens` → `status: incomplete`, `incomplete_details.reason: max_output_tokens`. Reasoning tokens count toward it.
- `text.verbosity` and `reasoning.effort` on GPT-5-family models; `temperature`/`top_p`/`frequency_penalty`/`presence_penalty`/`stop` on classic chat models.

## Set up
Optional: `azd env set DEPLOY_LEGACY_CHAT true && azd provision` adds a non-reasoning model so TODO 4 can measure temperature diversity.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Classifier with delimiters; add definitions + examples when `few_shot=True`. | Most quality wins come from the prompt, not the model. |
| 2 | Force truncation and read `status` / `incomplete_details`. | Truncated output is a silent production bug. |
| 3 | Compare `verbosity` low vs high. | Length control without prompt hacks. |
| 4 | Try `temperature` on the reasoning model; measure diversity on the legacy model if present. | Know which knobs exist for which model family. |

## Run and test
```bash
./lab run 18 && ./lab validate 18      # one click: ./lab solve 18
```

## Explore
- Add "think step by step" to the classifier and compare. Reasoning models already reason internally; raise `effort` instead.
- On the legacy model, try `frequency_penalty` (repetition) and `presence_penalty` (new topics), and `stop`.

## Exam reflexes
- Consistent, factual output → **low temperature** (change temperature *or* top_p, not both). Repetition → **frequency_penalty**. New topics → **presence_penalty**.
- Reasoning models → **reasoning effort** (and verbosity), not temperature.
- Cut-off answers → raise **max_output_tokens**, especially with reasoning models.

## Clean up
Nothing to clean.
