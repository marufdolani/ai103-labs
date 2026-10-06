# Lab 01 · Provision and tour the Foundry platform

**Scenario.** You lead the AI platform team at Contoso. Before onboarding five product teams you must prove the new Microsoft Foundry platform is wired correctly: one Foundry resource, one project, the right model deployments, Azure AI Search, Storage and Application Insights connected to the project.

**Exam objectives.** D1 › Set up AI solutions in Foundry: *design Azure infrastructure for AI apps*, *choose deployment options*, *configure model deployments*, *configure an application to connect to a Foundry project*.

**You will learn**
- The Foundry hierarchy: **resource** (`Microsoft.CognitiveServices/accounts`, kind `AIServices`) → **project** (`accounts/projects`) → **deployments** and **connections**.
- The four endpoints a Foundry resource exposes, and which client uses which.
- How to enumerate deployments and connections with the `azure-ai-projects` SDK.

## Set up
1. Deploy the platform once (repo root): `azd up` → pick your subscription and **eastus2**. Or use the **Deploy to Azure** button in the root README, then `./lab env-from-rg <resource-group>`.
2. `./lab doctor` should show every check green.
3. Open `infra/core.bicep` and find: the Foundry account, the project, the `deployments` loop, and the three project connections.

## Steps (edit `starter/lab.py`)
| TODO | What to build | Why it matters |
|---|---|---|
| 1 | List the project's model deployments (`project().deployments.list()`) and capture name, model, SKU and capacity. | Deployment name ≠ model name. Your code always calls the **deployment name**. |
| 2 | List the project connections (`project().connections.list()`). | Connections are how a project reaches Search, Storage, App Insights without secrets in code. |
| 3 | Get the Application Insights connection string from `project().telemetry`. | Tracing (labs 16, 38) uses it. |
| 4 | Send one prompt to the chat deployment with the Responses API through the project's OpenAI client. | Proves identity, RBAC and the project endpoint all work end to end. |

## Run and test
```bash
./lab run 01              # your starter
./lab validate 01         # tests your starter
./lab solve 01            # one click: runs + validates the reference solution
```

## Explore
- In the Foundry portal (ai.azure.com) open the project → **Models + endpoints** and compare with your table.
- Note the SKU column: every deployment is **GlobalStandard**. Which deployment type would you choose if processing had to stay in the EU? *(Data Zone Standard.)*

## Exam reflexes
- Project endpoint format: `https://<resource>.services.ai.azure.com/api/projects/<project>`.
- `model=` in API calls is the **deployment name**.
- Foundry resource = multi-service: models **and** Language, Speech, Translator, Vision, Content Safety, Document Intelligence, Content Understanding behind one endpoint.

## Clean up
Nothing to clean. Delete the whole platform at the end of the course with `azd down --purge`.
