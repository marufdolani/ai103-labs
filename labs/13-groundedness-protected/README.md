# Lab 13 · Groundedness and protected-material detection

**Scenario.** Contoso's HR assistant told an employee they'd get "12 weeks at half pay". The policy says 8 weeks fully paid. You'll catch fabrications two ways (the Content Safety **groundedness detection** API and an AI-assisted **Groundedness evaluator**) and check outputs for protected material.

**Exam objectives.** D1 › *Configure … risk detection*; *apply responsible AI instrumentation, including evaluators*. D2 › *Evaluate models and apps, including detecting fabrications*.

**You will learn**
- Runtime detection (an API you call per response, which can block or flag) vs offline evaluation (scores over a dataset).
- The groundedness request shape: `task: QnA | Summarization`, `qna.query`, `text`, `groundingSources`.
- Protected material detection for text (and code, with citations).

## Set up
Nothing extra. Groundedness detection is regional. If your region lacks it, the detector test is **skipped** and the evaluator still runs.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `detect_groundedness()` via `text:detectGroundedness`. | Real-time guard you could put before showing an answer. |
| 2 | `judge_groundedness()` with `GroundednessEvaluator` (1-5). | The same concept as a quality metric. |
| 3 | `protected_material()` via `text:detectProtectedMaterial`. | Stops the model reproducing copyrighted text. |

## Run and test
```bash
./lab run 13 && ./lab validate 13      # one click: ./lab solve 13
```

## Explore
- Set `"reasoning": true` (needs a linked Azure OpenAI deployment) to get explanations and a corrected answer.
- Use the Summarization task on a meeting transcript and a hallucinated summary.

## Exam reflexes
- "Response contains claims not in the sources" → **groundedness detection** (runtime) / **Groundedness evaluator** (offline).
- "Model reproduces lyrics, articles or licensed code" → **protected material detection**.

## Clean up
Nothing to clean.
