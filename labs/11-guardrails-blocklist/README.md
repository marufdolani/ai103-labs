# Lab 11 · Custom guardrail: thresholds, shields, blocklists

**Scenario.** Contoso Marketing's public chatbot must never mention competitors, must resist jailbreaks, and needs stricter harm thresholds than the default. You'll define a **guardrail** (RAI policy) in Bicep, attach it to a new deployment, and compare it with the default guardrail.

**Exam objectives.** D1 › Implement responsible AI: *configure safety filters, guardrails, risk detection, and content moderation*; *govern agent behaviour with … constraints*.

**You will learn**
- Guardrail anatomy: **risk** (hate, sexual, violence, self-harm, jailbreak, indirect attack, protected material, blocklist) × **intervention point** (prompt / completion; for agents also tool call and tool response) × **action** (annotate / block) × **threshold** (Low/Medium/High).
- Severity threshold semantics: `Low` blocks low *and above* (the strictest).
- Reading the `content_filter` error (input blocked) vs `finish_reason: content_filter` (output blocked).

## Set up (extra infrastructure, about 2 minutes)
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmarufdolani%2Fai103-labs%2Fmain%2Flabs%2F11-guardrails-blocklist%2Finfra%2Fazuredeploy.json)
```bash
source .env
az deployment group create -g $AZURE_RESOURCE_GROUP -n lab11-guardrail \
  -f labs/11-guardrails-blocklist/infra/guardrail.bicep -p foundryAccountName=$FOUNDRY_ACCOUNT_NAME
./lab env-merge $AZURE_RESOURCE_GROUP lab11-guardrail
```
Then open the Foundry portal → **Guardrails + controls** and find `strict-guardrail`.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `try_prompt()`: catch `BadRequestError` with code `content_filter` → input blocked; collect triggered filters. | Apps must handle a blocked prompt gracefully. |
| 2 | Detect output blocking (`finish_reason == "content_filter"`) and read prompt annotations. | Annotate-only filters still report what they saw. |

## Run and test
```bash
./lab run 11 && ./lab validate 11      # one click: ./lab solve 11
```

## Explore
- Agents get their own guardrail (`PromptAgentDefinition(rai_config=RaiConfig(rai_policy_name=...))`). It takes precedence over the model deployment's guardrail when the agent is called, and can add **tool call** and **tool response** intervention points.
- Switch `Protected Material Code` to annotate-only and look at the citation it returns for known public code.
- Streaming: **asynchronous filter** mode lowers latency; content is filtered after it streams.

## Exam reflexes
- Specific words or names → **custom blocklist**. Jailbreak in the user's own prompt → **Prompt Shields (user prompt attacks)**. Attack hidden in documents or tool output → **indirect attack** detection (lab 12).
- Strictest harm setting → threshold **Low**.

## Clean up
```bash
az cognitiveservices account deployment delete -g $AZURE_RESOURCE_GROUP -n $FOUNDRY_ACCOUNT_NAME --deployment-name guarded-chat
```
