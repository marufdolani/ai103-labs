# Lab 04 · Quotas, rate limits and resilient retries

**Scenario.** On launch day Contoso's assistant starts returning errors. Logs show HTTP **429 Too Many Requests**. You'll reproduce it on purpose, then make the client resilient with exponential backoff that honours `retry-after`, and add spillover to a second deployment.

**Exam objectives.** D1 › *Manage quotas, scaling, rate limits, and cost footprints for model and agent workloads*.

**You will learn**
- Quota is **tokens-per-minute (TPM)** and **requests-per-minute (RPM)** per deployment, per region, per subscription. Capacity units: 1 = 1,000 TPM.
- Azure estimates tokens **including `max_output_tokens`** when it admits a request.
- Retry etiquette: honour `retry-after`, add jitter, cap attempts, fall back.

## Set up
The platform includes a deliberately tiny deployment, `THROTTLED_MODEL` (capacity 1 = 1K TPM). The lab takes ~2 minutes because it waits for rate-limit windows to reset.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Read the throttled deployment's SKU and capacity. | Know your ceiling before you load-test. |
| 2 | Fire a burst with a **no-retry** client (`with_options(max_retries=0)`); count 429s and capture `retry-after`. | Shows the raw failure. |
| 3 | `call_with_backoff()`: catch `openai.RateLimitError`, sleep `retry-after` (or 2^n + jitter), retry. | The standard resilience pattern. |
| 4 | `call_with_spillover()`: on 429 send the request to `SMALL_MODEL` instead. | Same pattern as PTU spillover or an APIM backend pool. |

## Run and test
```bash
./lab run 04 && ./lab validate 04      # one click: ./lab solve 04
```

## Explore
- Lower `max_output_tokens` to 50 and rerun: fewer 429s, because admission estimates drop.
- Note the OpenAI SDK already retries twice by default (`max_retries=2`). Production apps tune this rather than writing loops by hand. You write it here to learn the mechanics.

## Exam reflexes
- 429 → **retry with exponential backoff + retry-after**, raise **quota**, spread across deployments/regions, or move steady load to **provisioned throughput (PTU)**.
- Global Standard = highest default quota; Data Zone = residency within EU/US; Batch = 50% cheaper, 24h, separate quota.

## Clean up
Nothing to clean.
