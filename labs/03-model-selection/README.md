# Lab 03 · Choose the right model: small, large, reasoning

**Scenario.** Three teams ask for "the best model". Support wants ticket triage at 50,000 tickets/day, engineering wants code generation, and finance wants multistep calculations. You'll benchmark a small model, a mid model and a large model on each task and recommend one per workload with data: accuracy, latency, tokens and cost.

**Exam objectives.** D1 › *Choose an appropriate model for each task, including LLMs, small language models, multimodal models*. D2 › *Deploy and consume LLMs, small models, code models*; *tune generation behaviour*.

**You will learn**
- How to measure latency and token usage (`usage.input_tokens`, `output_tokens`, `output_tokens_details.reasoning_tokens`).
- Why reasoning effort matters more than model size for multistep problems.
- How to turn token counts into a cost estimate per 1,000 requests.

## Set up
Deployments used: `SMALL_MODEL` (nano), `CHAT_MODEL` (mini), `LARGE_MODEL`. Prices in `solution/lab.py` are **illustrative**; check the Azure OpenAI pricing page for your agreement.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `run_task(model, task, effort)` that calls the Responses API and returns latency, tokens and the answer. | One harness for all comparisons. |
| 2 | Score each answer with the task's checker. | Accuracy first, then cost. |
| 3 | Compute cost per 1,000 requests from token counts and the price table. | Exam questions often hinge on cost at volume. |
| 4 | Run the logic task on the small model with `low` and `high` reasoning effort. | Effort trades latency and tokens for depth. |

## Run and test
```bash
./lab run 03 && ./lab validate 03      # one click: ./lab solve 03
```

## Explore
- Add `"verbosity": "low"` to `text=` and compare output tokens.
- Which model would you pick for 50,000 triage tickets/day? Multiply the cost per 1,000 by 50.

## Exam reflexes
- Narrow, high-volume, latency-sensitive → **small model**. Complex multistep → **reasoning model / higher reasoning effort**. Image input → **multimodal model**.
- Reasoning models: control depth with `reasoning.effort`, not `temperature`.
- Always measure on your own data: Foundry's model catalog benchmarks are a starting point, not a decision.

## Clean up
Nothing to clean.
