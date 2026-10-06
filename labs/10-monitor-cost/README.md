# Lab 10 · Monitor tokens, latency, drift and cost

**Scenario.** Finance asks: "What will the HR assistant cost at 100,000 requests a month, and how will we know if it gets slower or more expensive?" You'll measure token analytics in the client, read the Foundry resource's platform metrics, query Log Analytics with KQL, and set a budget alert.

**Exam objectives.** D1 › *Manage … cost footprints*; *monitor model performance, drift, safety events*. D2 › *Set up observability by implementing … token analytics … and latency breakdowns*.

**You will learn**
- Client-side analytics from `response.usage` (input, output, **reasoning** tokens) and latency percentiles.
- Platform metrics on the Foundry resource (Azure Monitor) and diagnostic export to Log Analytics (`AzureMetrics` table).
- Budgets and alerts as cost guardrails.

## Set up
The platform already sends Foundry logs and metrics to Log Analytics (see `foundryDiagnostics` in `infra/core.bicep`) and gives you Log Analytics Reader + Monitoring Reader.

Optional budget alert:
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmarufdolani%2Fai103-labs%2Fmain%2Flabs%2F10-monitor-cost%2Finfra%2Fazuredeploy.json)
```bash
az deployment group create -g $AZURE_RESOURCE_GROUP -f labs/10-monitor-cost/infra/budget.bicep -p contactEmail=you@contoso.com amount=50
```

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Generate traffic and capture latency + usage per call. | Your ground truth per request. |
| 2 | p50/p95 latency, average tokens, reasoning share, cost per request and per month. | The numbers finance and SRE ask for. |
| 3 | List metric definitions on the Foundry resource and query token metrics. | Platform view across every app using the resource. |
| 4 | KQL over `AzureMetrics` in Log Analytics. | Long-term retention, joins, alerts and workbooks. |

## Run and test
```bash
./lab run 10 && ./lab validate 10      # one click: ./lab solve 10
```
Re-run after 10-15 minutes to see Log Analytics rows; diagnostic export lags.

## Explore
- Create an Azure Monitor alert on a token metric (> N tokens in 5 minutes).
- Drift: lab 14 and lab 38 add **continuous evaluation** of production responses. Latency drift shows up here, quality drift there.
- Reasoning tokens are billed as output tokens. Watch `reasoning_share` when you raise effort.

## Exam reflexes
- Cost/usage per deployment → **Azure Monitor metrics** on the Foundry resource. Per-app chargeback → **APIM `llm-emit-token-metric`** (lab 06).
- End-to-end request traces → **Application Insights tracing** (labs 16, 38). Quality drift → **continuous evaluation**.

## Clean up
`az consumption budget delete --budget-name ai103-labs-monthly -g $AZURE_RESOURCE_GROUP` if you created one.
