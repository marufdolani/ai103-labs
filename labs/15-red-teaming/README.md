# Lab 15 · Automated red teaming

**Scenario.** Before launching Contoso's public assistant, security wants adversarial testing at scale, not five hand-written jailbreaks. You'll run the **AI Red Teaming Agent**: it generates attack objectives per risk category, transforms them with attack strategies (Base64, character flips and more), fires them at your app and scores the results.

**Exam objectives.** D1 › *Apply responsible AI instrumentation, including … safety evaluations*; *implement auditing* (attack evidence). D2 › *Evaluate … safety*.

**You will learn**
- Risk categories × attack strategies → **attack success rate (ASR)**.
- The target can be any callable: model, app or agent.
- Where red teaming fits: pre-release and on every major change, alongside evaluations (lab 14) and guardrails (lab 11).

## Set up
```bash
pip install -r requirements-redteam.txt      # needs Python 3.11 or 3.12 (PyRIT)
```
Runs take about 5-10 minutes. Results are logged to your Foundry project (Evaluation → AI red teaming) and saved to `.out/lab15/redteam.json`.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `target()`: the system under test. Treat a guardrail block as a successful defence. | Red-team the *app*, not just the model. |
| 2 | Configure `RedTeam` (risk categories, objectives) and `scan()` with attack strategies. | Breadth (categories) × depth (strategies). |
| 3 | Read the overall ASR from the scorecard. | One number to track release over release. |

## Run and test
```bash
./lab run 15 && ./lab validate 15      # one click: ./lab solve 15
```

## Explore
- Point `target` at the `GUARDED_MODEL` from lab 11 and compare ASR.
- Add `AttackStrategy.MODERATE` or `AttackStrategy.Jailbreak`. Use `AttackStrategy.Compose([...])` to chain transformations.

## Exam reflexes
- "Automated adversarial testing before release" → **AI Red Teaming Agent** (PyRIT). Metric: **attack success rate**.
- Red teaming finds weaknesses. Guardrails and system prompts fix them. Evaluations measure overall quality.

## Clean up
Nothing to clean.
