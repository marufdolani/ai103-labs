# Lab 25 · Fine-tuning: decide, prepare data, submit

**Scenario.** Contoso Support wants every reply in its brand voice. The current fix is a 3,000-token few-shot prompt on every call. You'll decide whether fine-tuning is the right tool, prepare and validate **SFT** and **DPO** datasets, upload them, and (optionally) submit a job.

**Exam objectives.** D2 › *Tune generation behaviour*; *deploy and consume … small models*. D1 › *Choose an appropriate model* and *choose deployment options* (fine-tuned deployments).

**You will learn**
- The optimisation ladder: **prompting → RAG → fine-tuning**, and which problem each solves.
- SFT chat format vs DPO preference format; RFT (reinforcement fine-tuning) for reasoning models with graders.
- Upload with `purpose="fine-tune"` and file processing states.

## Set up
Training data: `solution/sft_examples.jsonl` (12 rewrites) and `dpo_examples.jsonl` (3 preference pairs).
Submitting a job **costs money** and only works for base models that support fine-tuning in your region. The lab uploads by default and submits only with:
```bash
RUN_FINE_TUNE=true FT_BASE_MODEL=<base model and version from the portal> ./lab run 25 --solution
```

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Map five scenarios to prompting / RAG / SFT / DPO / RFT. | The exam asks this constantly. |
| 2 | SFT records (`messages`: system, user, assistant). | The standard chat fine-tuning format. |
| 3 | DPO records (`input`, `preferred_output`, `non_preferred_output`). | Learn from human preference pairs. |
| 4 | Validate before upload. | Bad lines fail jobs after you've waited in the queue. |
| 5 | Upload and wait for `processed`. | Same flow in the portal, SDK and REST. |

## Run and test
```bash
./lab run 25 && ./lab validate 25      # one click: ./lab solve 25
./lab clean 25                         # deletes uploaded training files
```

## Explore
- After training, deploy the fine-tuned model with the **Developer** deployment type for cheap evaluation before a Standard deployment.
- Evaluate base vs fine-tuned with lab 14's evaluators. A fine-tune is only "better" if the evaluation says so.

## Exam reflexes
- Knowledge that changes → **RAG**. Style, format, tone, shorter prompts → **SFT**. Human preference pairs → **DPO**. Reasoning with automatic graders → **RFT**.
- Fine-tuning doesn't fix missing facts. Try prompting first.

## Clean up
`./lab clean 25`. Delete any fine-tuned deployment you created (it bills hourly hosting).
