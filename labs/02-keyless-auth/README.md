# Lab 02 · Keyless access with Entra ID and disabled keys

**Scenario.** Contoso's security review bans API keys and secrets in AI apps. You must prove the platform works with Microsoft Entra ID tokens only, and that key-based calls are refused.

**Exam objectives.** D1 › Manage, monitor, and secure AI systems: *configure security, including managed identity, keyless credentials, and role policies*.

**You will learn**
- How `DefaultAzureCredential` picks an identity (developer login locally, managed identity in Azure).
- What's inside an Entra access token (`aud`, `oid`, `tid`) and which scope Foundry Tools use.
- How `disableLocalAuth: true` on the Foundry resource blocks every key-based request.

## Set up
- Platform deployed (lab 01). The Bicep sets `disableLocalAuth: true` on the Foundry resource. Search `infra/core.bicep` for it.
- You're signed in with `az login` (or `azd auth login`).

## Steps (edit `starter/lab.py`)
| TODO | Build | Why |
|---|---|---|
| 1 | Get a token for `https://cognitiveservices.azure.com/.default` and decode its claims. | This scope covers models **and** all Foundry Tools. The project/agent APIs use `https://ai.azure.com/.default` (the SDK handles it). |
| 2 | Call the small model through `aoai()` (OpenAI client whose `api_key` is a **token provider**). | Keyless pattern for the OpenAI SDK: `get_bearer_token_provider(credential, scope)`. |
| 3 | Call the same endpoint with an `api-key` header and record the HTTP status. | Expect 401/403. With local auth disabled even a *real* key would fail. |
| 4 | Read `properties.disableLocalAuth` from Azure Resource Manager. | Auditors check this property (Azure Policy can enforce it). |

## Run and test
```bash
./lab run 02 && ./lab validate 02      # or one click: ./lab solve 02
```

## Explore
- In production your app runs with a **managed identity**: assign it **Foundry User** (or Cognitive Services User for Foundry Tools only) on the resource. No code changes, `DefaultAzureCredential` picks it up.
- Azure Policy: *"Azure AI Services resources should have key access disabled"*.
- Speech SDK keyless: `SpeechConfig(token_credential=cred, endpoint=<custom-domain endpoint>)` needs a **custom subdomain** (ours has one).

## Exam reflexes
- "No secrets / no keys / rotate nothing" → **managed identity + RBAC + DefaultAzureCredential + disableLocalAuth**. Key Vault is a distractor: it still stores a key.
- Keyless requires a **custom subdomain** endpoint (not the regional endpoint).

## Clean up
Nothing to clean.
