# Lab 24 · Hybrid LLM + rules engine, multi-model orchestration

**Scenario.** Contoso Finance wants AI to process free-text expense claims, but auditors insist that approval decisions follow POL-FIN-004 exactly, every time. You'll let models do what they're good at (reading messy text, explaining decisions) and keep the decision in a deterministic rules engine. A cheap model extracts first and escalates to a large model when unsure.

**Exam objectives.** D2 › *Orchestrate multiple models, flows, or hybrid LLM and rules engines*; *design … tool-augmented flows*.

**You will learn**
- Separation of concerns: **LLM extracts → rules decide → LLM explains**.
- Confidence-based escalation from a small to a large model (cost control with a quality floor).
- Why "the LLM approved it" is never an acceptable audit answer.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `extract()`: Pydantic `Claim` with nullable fields and a confidence score. | Typed input for the rules engine. |
| 2 | `extract_with_escalation()`: small model first, large model if confidence < 0.7. | Pay for the big model only when needed. |
| 3 | `apply_policy()`: the deterministic rules (CFO escalation, cabin class, hotel caps, alcohol, receipts). | Auditable, testable, repeatable. |

## Run and test
```bash
./lab run 24 && ./lab validate 24      # one click: ./lab solve 24
```

## Explore
- Write an ambiguous claim ("flight to Asia, long one, fancy seat") and watch escalation trigger.
- Swap the rules engine for a real one (for example, a decision table in Dataverse or Azure Logic Apps) and keep the same contract.

## Exam reflexes
- Strict business rules + unstructured input → **hybrid: LLM for extraction, rules/code for decisions**.
- Mixed difficulty at volume → **route by difficulty** (your own escalation, or model router in lab 05).

## Clean up
Nothing to clean.
