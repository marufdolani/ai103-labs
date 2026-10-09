# AI-103 Hands-On Labs

Fifty scenario-based labs for **Exam AI-103: Developing AI Apps and Agents on Azure**. Every lab is a realistic Contoso scenario mapped to the official skills outline (16 April 2026). Each one has step-by-step instructions, a starter you complete, a reference solution and automated tests that check your work against live Azure resources.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/marufdolani/ai103-labs)
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmarufdolani%2Fai103-labs%2Fmain%2Finfra%2Fazuredeploy.json)

## How it works

```
infra/        one shared platform: Foundry resource + project, models, AI Search, Storage, App Insights, keyless RBAC
labs/NN-*/    README.md (scenario + steps) · starter/lab.py (you) · solution/lab.py (reference) · test_lab.py (validation)
labkit/       shared clients (all keyless), helpers and the ./lab CLI
```

1. **Deploy once.** `azd up` (or the Deploy to Azure button) creates the shared platform and writes `.env`.
2. **Do a lab.** Read the lab README, then fill in each `# TODO n` block in `starter/lab.py`.
3. **Validate.** `./lab validate NN` runs that lab's tests against *your* code and live resources.
4. **Check the answer in one click.** `./lab solve NN` runs the reference solution and the same tests, so you can compare outputs.

```bash
./lab list               # all 50 labs by exam domain
./lab open 20            # where the files are
./lab run 20             # run your starter
./lab validate 20        # test your implementation
./lab solve 20           # one click: reference solution + tests
./lab clean 20           # delete what the lab created
./lab validate-all --solution   # run the whole reference suite
```

## Quick start

**Option A: Codespaces (nothing to install).** Click *Open in GitHub Codespaces*, then in the terminal:
```bash
azd auth login && az login
azd up                 # environment name: ai103 · region: eastus2 · ~10 minutes
./lab doctor           # checks settings, identity, models, search and storage
```

**Option B: local (Windows, macOS, Linux).** Python 3.11–3.12, [Azure Developer CLI](https://aka.ms/azd), Azure CLI.
```bash
git clone https://github.com/marufdolani/ai103-labs && cd ai103-labs
azd auth login && az login
azd up                 # postprovision creates .venv, installs requirements, writes .env, generates starters
./lab doctor           # Windows: .venv\Scripts\activate then  python -m labkit doctor
```

**Option C: Deploy to Azure button.** Deploys the same platform into a resource group you choose. Enter your object ID (`az ad signed-in-user show --query id -o tsv`) so you get data-plane roles. Then:
```bash
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./lab env-from-rg <your-resource-group>    # writes .env from the deployment outputs
./lab make-starters && ./lab doctor
```

> **Keyless by design.** API keys are disabled on the Foundry resource and Storage. Every lab authenticates with Microsoft Entra ID (`DefaultAzureCredential`). New role assignments can take ~5 minutes to apply; rerun `./lab doctor` if a check fails.

## Learning plan

The labs follow the exam domains, but they're grouped below into **scenario tracks** that build on each other. Total hands-on time is about **23 hours**.

For a 48-hour exam cram alongside the labs, download [`docs/AI-103-Fast-Track.html`](docs/AI-103-Fast-Track.html) (study plan, reflex map, scenario drills, code patterns, exam traps) and open it in a browser. A one-page table [cheatsheet](docs/AI-103-Cheatsheet.html) is alongside it.

| Track | Labs | Scenario thread | Exam weight |
|---|---|---|---|
| 1 · Platform & governance | 01–04, 09 | Stand up Contoso's AI platform: keyless, right-sized, least privilege | 25–30% |
| 2 · Build generative apps | 17–21 | HR policy assistant: chat, prompts, schema output, RAG, tools | 30–35% |
| 3 · Make it reliable | 22–26, 14, 07 | Pipelines, reflection, hybrid rules, fine-tuning decision, evaluation gates in CI | |
| 4 · Agents | 27–33 | Versioned agents with File Search, Code Interpreter, functions, OpenAPI, MCP, AI Search | |
| 5 · Multi-agent & autonomy | 34–38 | Orchestration patterns, A2A, approvals, tracing and agent evaluation | |
| 6 · Responsible AI & ops | 11–13, 15, 16, 10, 05, 06, 08 | Guardrails, shields, red teaming, audit, monitoring, gateway, private networking | |
| 7 · Vision | 39–43 | Marketing images/video, visual Q&A, Content Understanding, multimodal safety | 10–15% |
| 8 · Text & speech | 44–47 | Multilingual reviews, translation, call transcripts, voice concierge | 10–15% |
| 9 · Information extraction | 48–49 | Scanned bulletins and invoices into grounded, searchable knowledge | 10–15% |
| 10 · Capstone | 50 | Governed, grounded, audited knowledge agent with a release gate | all |

**Suggested schedules**
- **Two weeks, ~2 hours a day:** one track per day; use days 11–14 for the capstone, redoing failed validations, and scenario drills.
- **Five-day sprint:** Day 1 tracks 1–2 · Day 2 tracks 3–4 · Day 3 tracks 5–6 · Day 4 tracks 7–9 · Day 5 capstone + mock exam.
- **Exam in 48 hours:** do labs 01, 17, 19, 20, 21, 27, 32, 33, 11, 12, 14, 41, 42, 44, 46, 48, 49 and 50 (about 8 hours). Run `./lab solve NN` on the rest and read their *Exam reflexes* sections.

Every lab README has the same sections: **Scenario · Exam objectives · You will learn · Steps (TODO table) · Run and test · Explore · Exam reflexes · Clean up.**

## The 50 labs

### D1 · Plan and manage an Azure AI solution (25-30%)

| Lab | Scenario | Time | Needs |
|---|---|---|---|
| [01](labs/01-platform-tour/README.md) | Provision and tour the Foundry platform | 20 min |  |
| [02](labs/02-keyless-auth/README.md) | Keyless access with Entra ID and disabled keys | 20 min |  |
| [03](labs/03-model-selection/README.md) | Choose the right model: small, large, reasoning | 25 min |  |
| [04](labs/04-quotas-429/README.md) | Quotas, rate limits and resilient retries | 20 min |  |
| [05](labs/05-model-router/README.md) | Route prompts with model router | 15 min | model router |
| [06](labs/06-ai-gateway/README.md) | AI gateway: per-app token limits with API Management | 45 min | extra infra: APIM |
| [07](labs/07-cicd-eval-gate/README.md) | CI/CD for Foundry with an evaluation gate | 35 min |  |
| [08](labs/08-private-networking/README.md) | Network-isolate the AI platform | 40 min | extra infra: VNet |
| [09](labs/09-rbac-least-privilege/README.md) | Least-privilege RBAC for AI teams | 25 min |  |
| [10](labs/10-monitor-cost/README.md) | Monitor tokens, latency, drift and cost | 30 min |  |
| [11](labs/11-guardrails-blocklist/README.md) | Custom guardrail: thresholds, shields, blocklists | 30 min | extra infra: guardrail |
| [12](labs/12-prompt-shields/README.md) | Prompt Shields: direct and indirect attacks | 20 min |  |
| [13](labs/13-groundedness-protected/README.md) | Groundedness and protected-material detection | 20 min |  |
| [14](labs/14-evaluate-quality-safety/README.md) | Quality and safety evaluations | 30 min |  |
| [15](labs/15-red-teaming/README.md) | Automated red teaming | 30 min |  |
| [16](labs/16-audit-trail/README.md) | Audit trail: traces, provenance, approvals | 25 min |  |

### D2 · Implement generative AI and agentic solutions (30-35%)

| Lab | Scenario | Time | Needs |
|---|---|---|---|
| [17](labs/17-responses-chat/README.md) | Chat app with the Responses API | 20 min |  |
| [18](labs/18-prompt-parameters/README.md) | Prompt engineering and generation parameters | 25 min |  |
| [19](labs/19-structured-outputs/README.md) | Structured outputs for downstream systems | 20 min |  |
| [20](labs/20-rag-from-scratch/README.md) | RAG from scratch with hybrid and semantic search | 40 min |  |
| [21](labs/21-function-calling/README.md) | Function calling loop | 25 min |  |
| [22](labs/22-multistep-pipeline/README.md) | Multistep reasoning pipeline | 25 min |  |
| [23](labs/23-reflection-loop/README.md) | Reflection and self-critique loop | 25 min |  |
| [24](labs/24-hybrid-rules-orchestration/README.md) | Hybrid LLM + rules engine, multi-model orchestration | 30 min |  |
| [25](labs/25-fine-tuning-prep/README.md) | Fine-tuning: decide, prepare data, submit | 30 min |  |
| [26](labs/26-evaluate-rag-variants/README.md) | Evaluate and compare app variants | 30 min |  |
| [27](labs/27-first-agent/README.md) | First prompt agent with versions | 20 min |  |
| [28](labs/28-agent-file-search/README.md) | Agent with File Search | 20 min |  |
| [29](labs/29-agent-code-interpreter/README.md) | Agent with Code Interpreter | 20 min |  |
| [30](labs/30-agent-functions-memory/README.md) | Agent with custom functions and memory | 30 min |  |
| [31](labs/31-agent-openapi/README.md) | Agent with an OpenAPI tool | 20 min |  |
| [32](labs/32-agent-mcp-approval/README.md) | Agent with MCP: approvals and allow-lists | 25 min |  |
| [33](labs/33-agent-search-grounding/README.md) | Agent grounded on Azure AI Search | 25 min |  |
| [34](labs/34-multiagent-sequential-concurrent/README.md) | Multi-agent: sequential and concurrent | 30 min |  |
| [35](labs/35-multiagent-handoff-groupchat/README.md) | Multi-agent: handoff, group chat, Magentic | 35 min |  |
| [36](labs/36-a2a-delegation/README.md) | Agent-to-agent (A2A) discovery and delegation | 30 min |  |
| [37](labs/37-approval-workflow/README.md) | Semi-autonomous workflow with safeguards | 30 min |  |
| [38](labs/38-agent-observability/README.md) | Agent tracing, evaluation and error analysis | 30 min |  |

### D3 · Implement computer vision solutions (10-15%)

| Lab | Scenario | Time | Needs |
|---|---|---|---|
| [39](labs/39-image-generation/README.md) | Generate and edit images | 25 min | image model |
| [40](labs/40-video-generation/README.md) | Generate and remix video | 30 min | Sora |
| [41](labs/41-multimodal-understanding/README.md) | Captions, visual Q&A and alt text | 25 min |  |
| [42](labs/42-content-understanding-visual/README.md) | Content Understanding for images and video | 35 min |  |
| [43](labs/43-multimodal-safety/README.md) | Responsible AI for images | 25 min |  |

### D4 · Implement text analysis solutions (10-15%)

| Lab | Scenario | Time | Needs |
|---|---|---|---|
| [44](labs/44-language-analysis/README.md) | Text analysis: Language service vs LLM | 30 min |  |
| [45](labs/45-translation/README.md) | Translate text and documents | 30 min |  |
| [46](labs/46-speech-basics/README.md) | Speech to text, text to speech, SSML, translation | 30 min |  |
| [47](labs/47-voice-agent/README.md) | Speech as an agent modality | 30 min | audio models |

### D5 · Implement information extraction solutions (10-15%)

| Lab | Scenario | Time | Needs |
|---|---|---|---|
| [48](labs/48-search-enrichment/README.md) | Ingestion with skillsets and integrated vectorization | 45 min |  |
| [49](labs/49-document-extraction/README.md) | Document Intelligence vs Content Understanding | 35 min |  |
| [50](labs/50-capstone/README.md) | Capstone: governed, grounded knowledge agent | 60 min |  |

## Optional capabilities

The core platform deploys a chat model, a small model, a large multimodal model, an embedding model and model router. Labs that need more are **skipped, not failed**, until you enable them:

| Requirement | Setting in `.env` | How to enable |
|---|---|---|
| `router` | `ROUTER_MODEL` | `azd env set DEPLOY_MODEL_ROUTER true && azd provision` |
| `image` | `IMAGE_MODEL` | `azd env set DEPLOY_IMAGE_MODEL true && azd provision` |
| `video` | `VIDEO_MODEL` | `azd env set DEPLOY_VIDEO_MODEL true && azd provision` |
| `audio` | `AUDIO_MODELS_ENABLED` | `azd env set DEPLOY_AUDIO_MODELS true && azd provision` |
| `legacy` | `LEGACY_CHAT_MODEL` | `azd env set DEPLOY_LEGACY_CHAT true && azd provision` |
| `apim` | `APIM_GATEWAY_URL` | `deploy labs/06-ai-gateway/infra (see the lab README)` |
| `guarded` | `GUARDED_MODEL` | `deploy labs/11-guardrails-blocklist/infra (see the lab README)` |
| `network` | `ISOLATED_FOUNDRY_NAME` | `deploy labs/08-private-networking/infra (see the lab README)` |

Labs 06, 08, 10 and 11 have their own **Deploy to Azure** buttons for the extra infrastructure. See each lab's README.

## Cost

Estimates only (verify in the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/)); not measured spend.

| Scenario | Estimated total |
|---|---|
| All 50 labs, torn down within 3-4 days | **USD 25-45** |
| Platform left up for two weeks | **USD 80-130** |

| Driver | Estimate |
|---|---|
| Idle platform (Search Basic ~USD 75/month, plus Log Analytics, App Insights, Storage) | ~USD 2.5-3.5/day |
| API Management (lab 06) | ~USD 0.20/hour while deployed |
| Private endpoints and VNet (lab 08) | ~USD 0.50-1/day |
| Model tokens (chat, embeddings, evaluators, red teaming) | ~USD 8-15 in total |
| Optional Sora and image models | USD 5-20, depending on clips rendered |
| Content Understanding, Document Intelligence, Translator, Speech, Language | cents per lab |

Run `./lab clean N` after each lab, delete the lab 06 and 08 extras straight after those labs, and set the lab 10 budget alert. Tear everything down with:
```bash
azd down --purge
```

## Validation status

- Bicep templates compile and lint clean (Bicep 0.48), and the `azuredeploy.json` files are regenerated from them.
- Python code compiles, and SDK calls were checked against these versions: `azure-ai-projects` 2.8, `openai` 3.24, `agent-framework` 1.20, `azure-ai-evaluation` 1.18, `azure-ai-translation-*` 2.0, `azure-search-documents` 11.6/12.0, `azure-cognitiveservices-speech` 1.52.
- The labs **have not yet been run end to end against a live subscription**. Model names and versions are parameters in `infra/core.bicep` (`chatModel`, `chatModelVersion`, …). If `azd up` reports a model or version isn't available in your region, change the parameter and run `azd provision` again. Preview features (Sora, guardrail intervention points, A2A tool, Content Understanding pro mode) change often; the lab READMEs say where.
- Tests that call generative models check behaviour (grounding, citations, schema, blocked attacks), not exact wording, so an occasional rerun may be needed.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `PROJECT_ENDPOINT is not set` | Run `azd up`, or `./lab env-from-rg <rg>` after a portal deployment. |
| `403` / `PermissionDenied` right after deploying | Role assignments propagate in ~5 minutes. Run `./lab doctor` again. |
| `DeploymentNotFound` or quota errors in `azd up` | Lower capacities or change model versions in `infra/core.bicep`, then `azd provision`. |
| Lab says *skipped: 'image' not configured* | Enable the optional capability (table above) or run `./lab solve` on another lab. |
| Speech SDK error on Linux | `sudo apt-get install -y libasound2` (the dev container installs it). |
| Red-team lab won't install | Use Python 3.11/3.12 and `pip install -r requirements-redteam.txt`. |

## Sources

- [AI-103 study guide (skills measured)](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-103)
- Course learning paths: [generative AI apps](https://learn.microsoft.com/en-us/training/paths/develop-generative-ai-apps/), [AI agents](https://learn.microsoft.com/en-us/training/paths/develop-ai-agents-azure/), [natural language](https://learn.microsoft.com/en-us/training/paths/develop-language-solutions-azure-ai/), [visual data](https://learn.microsoft.com/en-us/training/paths/insight-visual-data/)
- [Course video playlist](https://www.youtube.com/playlist?list=PLWGIg_TYLeEQ) · [Microsoft Foundry documentation](https://learn.microsoft.com/en-us/azure/foundry/)
