# Lab 22 · Multistep reasoning pipeline

**Scenario.** Contoso's SRE team spends hours writing postmortems from incident logs. You'll build a pipeline that extracts facts, computes the outage duration deterministically, drafts the postmortem, verifies it against the facts with a stronger model, and fixes it once if needed.

**Exam objectives.** D2 › *Design workflows, tool-augmented flows, and multistep reasoning pipelines*; *orchestrate multiple models, flows, or hybrid LLM and rules engines*.

**You will learn**
- Prompt chaining with typed hand-offs (structured outputs between steps).
- Putting **deterministic tools** where models are weak (date arithmetic).
- Model-per-step: small model to extract, mid model to draft, large model to verify.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Extract `Facts` with the small model. | Cheap and structured; everything downstream depends on it. |
| 2 | Compute outage minutes in Python. | Correct by construction. |
| 3 | Draft with required sections from facts only. | Constrain the generator. |
| 4 | Verify with the large model; one fix pass if claims are unsupported. | A bounded self-correction loop. |

## Run and test
```bash
./lab run 22 && ./lab validate 22      # one click: ./lab solve 22
```

## Explore
- Run all steps on the small model and compare verification failures.
- Turn the pipeline into a Foundry **workflow agent** (portal → Agents → Workflows) with the same steps as nodes.

## Exam reflexes
- Multistep task with known stages → **sequential pipeline / workflow**. Open-ended planning → **Magentic orchestration** (lab 35).
- Arithmetic, dates, policy rules → **code/tools**, not the LLM.

## Clean up
Nothing to clean.
