# Lab 05 · Route prompts with model router

**Scenario.** Contoso's internal assistant gets everything from "what's the Wi-Fi password policy?" to "design a migration plan". Paying large-model prices for every prompt wastes budget. You'll put **model router** in front and observe which underlying model answers each prompt.

**Exam objectives.** D1 › *Choose the appropriate Foundry services for generative tasks*; *manage cost footprints*. D2 › *Orchestrate multiple models*.

**You will learn**
- Model router is **one deployment** that picks an underlying chat model per request.
- The response's `model` field reveals the model that actually answered.
- Where routing fits next to APIM load balancing (lab 06) and your own orchestration (lab 24).

## Set up
Needs `ROUTER_MODEL` (deployed by default). If `./lab doctor` shows it off: `azd env set DEPLOY_MODEL_ROUTER true && azd provision`.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Send each prompt to the router with Chat Completions and time it. | Router is called like any chat deployment. |
| 2 | Record `response.model` and token usage per prompt. | That's your evidence of routing and cost. |

## Run and test
```bash
./lab run 05 && ./lab validate 05      # one click: ./lab solve 05
```

## Explore
- In the portal, open the router deployment: newer versions let you set a **routing mode** (balanced, quality, cost) and a model subset. Re-run and compare.
- Compare total tokens with sending every prompt to `LARGE_MODEL`.

## Exam reflexes
- "Send each prompt to the cheapest capable model, single endpoint" → **model router**.
- "Spread load across regions/deployments, per-app quotas" → **API Management AI gateway** (lab 06), not model router.

## Clean up
Nothing to clean.
