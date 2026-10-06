# Lab 14 · Quality and safety evaluations

**Scenario.** Before Contoso's HR assistant goes live, the responsible-AI board wants evidence: are answers grounded, relevant, coherent, close to the reference answers, and free of harmful content? You'll run a batch evaluation with five kinds of evaluator and publish the results to the Foundry project.

**Exam objectives.** D1 › *Apply responsible AI instrumentation, including evaluators, safety evaluations, and explanation tooling*. D2 › *Evaluate models and apps, including detecting fabrications, relevance, quality, and safety*.

**You will learn**
- Evaluator families: **AI-assisted quality** (Groundedness, Relevance, Coherence, Fluency, Similarity), **NLP/math** (F1, BLEU, ROUGE, METEOR, GLEU), **risk and safety** (Violence, Hate/Unfairness, Sexual, Self-harm, Protected material, Indirect attack), **agent** (lab 38).
- Which evaluators need `context` or `ground_truth`.
- Each AI-assisted score comes with a `*_reason`: that's your **explanation tooling**.

## Set up
`solution/dataset.jsonl` has five rows. One response (`q4`) is a deliberate fabrication.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Build the evaluator dictionary. Safety evaluators take `azure_ai_project` + credential, not a judge model. | Microsoft hosts the safety models; quality judges use *your* deployment. |
| 2 | `evaluate(data=..., evaluators=..., azure_ai_project=...)`. | Batch run, aggregated metrics, results visible in the portal. |
| 3 | Pull per-row groundedness and find the fabrication. | Aggregates hide individual failures; error analysis starts per row. |

## Run and test
```bash
./lab run 14 && ./lab validate 14      # one click: ./lab solve 14
```
Open the printed portal link and read the `groundedness_reason` for `q4`.

## Explore
- Add `target=` to `evaluate()` so it calls your app for each query instead of using stored responses.
- **Continuous evaluation**: `project().evaluation_rules` can score a sample of live agent traffic on a schedule, which is how you catch drift.

## Exam reflexes
- Fabrication → **Groundedness**. Off-topic → **Relevance**. Compare with a reference answer → **Similarity / F1 / BLEU / ROUGE** (needs ground truth).
- Harmful content in outputs → **safety evaluators** (project-hosted). Adversarial probing → **AI red teaming** (lab 15).

## Clean up
Evaluation runs stay in the project for audit. Delete them in the portal if you want.
