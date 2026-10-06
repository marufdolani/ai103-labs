# Lab 06 · AI gateway: per-app token limits with API Management

**Scenario.** Thirty internal apps will share Contoso's model deployments. Finance wants chargeback, and one noisy app must not starve the others. You'll put **Azure API Management** in front of Foundry as an AI gateway: managed identity to the backend, and a **token-per-minute limit per consumer**.

**Exam objectives.** D1 › *Manage quotas, scaling, rate limits, and cost footprints*; *design Azure infrastructure for AI apps*; *configure security (managed identity, keyless credentials)*.

**You will learn**
- `authentication-managed-identity`: APIM calls Foundry with its own identity; consumers never see a model key.
- `llm-token-limit`: TPM limits keyed by subscription (or any expression, such as an Entra app ID).
- How a gateway isolates consumers that share one deployment.

## Set up (extra infrastructure, ~5 minutes, about USD 0.20/hour while it exists)
Deploy the gateway into your lab resource group, then merge its outputs into `.env`:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmarufdolani%2Fai103-labs%2Fmain%2Flabs%2F06-ai-gateway%2Finfra%2Fazuredeploy.json)

or from the CLI:
```bash
source .env
az deployment group create -g $AZURE_RESOURCE_GROUP -n lab06-apim \
  -f labs/06-ai-gateway/infra/apim.bicep \
  -p foundryAccountName=$FOUNDRY_ACCOUNT_NAME publisherEmail=you@contoso.com
./lab env-merge $AZURE_RESOURCE_GROUP lab06-apim      # portal deployments: use the deployment name shown in the portal
```
Read `infra/apim.bicep`: find the role assignment, the wildcard operations, the policy XML and the two subscriptions.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Fetch the `app-a` and `app-b` subscription keys from ARM (`listSecrets`). | These are *gateway* keys for consumers, not model keys. |
| 2 | Build an OpenAI client whose `base_url` is the gateway and that sends `Ocp-Apim-Subscription-Key`. | Apps change one URL; the SDK is unchanged. |
| 3 | Burst app-a until the gateway returns 429; read `x-remaining-tokens`. | The gateway enforces the budget before the model is called. |
| 4 | Call once as app-b. | A separate counter: app-b is unaffected. |

## Run and test
```bash
./lab run 06 && ./lab validate 06      # one click: ./lab solve 06
```

## Explore
- Add `<llm-emit-token-metric>` with a `Subscription ID` dimension and an Application Insights logger for chargeback dashboards.
- Add a second backend and a **backend pool** with circuit breaker for multi-region load balancing.
- `llm-semantic-cache-lookup/store` returns cached answers for similar prompts.

## Exam reflexes
- "Per-app token quotas, chargeback, load balancing across regions, one entry point" → **APIM AI gateway** (`llm-token-limit`, `llm-emit-token-metric`, backend pools).
- Gateway → model auth: **managed identity** (`authentication-managed-identity`).

## Clean up
```bash
az apim delete -g $AZURE_RESOURCE_GROUP -n <apim-name> --yes
```
