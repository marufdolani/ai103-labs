# Lab 07 · CI/CD for Foundry with an evaluation gate

**Scenario.** A developer "improved" the HR assistant's system prompt and quality dropped in production. Contoso now requires every prompt or model change to pass an automated evaluation before merge. You'll build the gate and wire it into GitHub Actions with keyless OIDC login.

**Exam objectives.** D1 › *Integrate Foundry projects with CI/CD pipelines*. D2 › *Evaluate models and apps, including detecting fabrications, relevance, quality*.

**You will learn**
- AI-assisted evaluators (Groundedness, Relevance) plus a deterministic check, aggregated into release thresholds.
- Why a gate needs a **known-bad variant**: proof that it actually catches regressions.
- GitHub Actions → Azure with **workload identity federation** (no secrets), and `azd pipeline config` as the shortcut.

## Set up
Files in `solution/` (copied to `starter/`): `eval_set.jsonl` (test cases), `prompt_good.txt`, `prompt_bad.txt`, `gate.json` (thresholds).

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `answer()`: the app under test, which answers from supplied context. | Evaluate the real app path, not the model alone. |
| 2 | Score each response: Groundedness, Relevance and a `must_contain` check. | Mix AI judges with cheap deterministic assertions. |
| 3 | `gate()`: compare means with `gate.json`. | Turns scores into a pass/fail release decision. |

## Run and test
```bash
./lab run 07 && ./lab validate 07      # one click: ./lab solve 07
```

## Wire it into GitHub Actions (optional, about 10 minutes)
The workflow is `.github/workflows/ai103-eval-gate.yml`.
```bash
# Easiest: azd creates the Entra app, federated credential and repo variables for you
azd pipeline config --provider github

# Or manually:
APP_ID=$(az ad app create --display-name ai103-gate --query appId -o tsv)
az ad sp create --id $APP_ID
az ad app federated-credential create --id $APP_ID --parameters '{"name":"main","issuer":"https://token.actions.githubusercontent.com","subject":"repo:<owner>/ai103-labs:ref:refs/heads/main","audiences":["api://AzureADTokenExchange"]}'
az role assignment create --assignee $APP_ID --role "Foundry User" --scope $FOUNDRY_RESOURCE_ID
gh variable set AZURE_CLIENT_ID -b $APP_ID      # plus AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID,
                                                # PROJECT_ENDPOINT, FOUNDRY_ENDPOINT, FOUNDRY_OPENAI_ENDPOINT, CHAT_MODEL, LARGE_MODEL
gh workflow run ai103-eval-gate
```
Then edit `prompt_good.txt` to something bad, push to a branch, and watch the gate fail.

## Explore
- Agents are versioned (`create_version`). A pipeline can create a new version, evaluate it, and only then point production at it.
- Infrastructure goes through the same pipeline: `azd provision` with this repo's Bicep.

## Exam reflexes
- CI/CD for AI = **IaC (Bicep/azd) + evaluation gate + versioned prompts/agents**, with **OIDC federated identity** instead of stored secrets.
- Fabrication check → **Groundedness**; on-topic → **Relevance**; reference answer → **Similarity/F1**.

## Clean up
Delete the Entra app if you created one: `az ad app delete --id $APP_ID`.
