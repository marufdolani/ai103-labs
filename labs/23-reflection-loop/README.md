# Lab 23 · Reflection and self-critique loop

**Scenario.** Contoso's support team drafts outage apology emails with a cheap model. Drafts often blame a vendor, use jargon or forget the discount code. You'll add a **critic** model with a rubric, and loop generate → critique → revise until the email passes.

**Exam objectives.** D2 › *Implement model reflection, chain-of-thought evaluations, and self-critique loops*; *tune generation behaviour*.

**You will learn**
- Evaluator-optimizer pattern: a separate critic with an explicit rubric, typed feedback, and stop conditions (target score, max rounds).
- Using a **different, stronger** model as critic to avoid grading your own homework.
- Reasoning **summaries** (`reasoning.summary`) as a transparent window into the critic's evaluation, without exposing raw chain-of-thought.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Generator: first draft, then revisions driven by issues. | Feedback must be specific to be actionable. |
| 2 | Critic: `responses.parse` with a `Critique` schema; collect reasoning summaries. | Structured scores you can threshold. |
| 3 | The bounded loop. | Reflection without bounds burns tokens. |

## Run and test
```bash
./lab run 23 && ./lab validate 23      # one click: ./lab solve 23
```

## Explore
- Use the same small model as critic. Does it score its own drafts higher?
- Record token usage per round: reflection multiplies cost. Is round 3 worth it?

## Exam reflexes
- "Improve quality by having the model review and revise" → **reflection / self-critique loop** with a rubric and a max-iterations bound.
- Reasoning models expose **reasoning summaries**, not raw chain-of-thought.

## Clean up
Nothing to clean.
