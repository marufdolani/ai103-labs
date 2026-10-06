# Lab 33 · Agent grounded on Azure AI Search

**Scenario.** Contoso's enterprise policy agent must use the governed search index (hybrid + semantic ranking), cite its sources, and never reveal HR-restricted documents to regular staff. You'll connect agents to Azure AI Search through a **project connection** and enforce **security trimming** with a filter.

**Exam objectives.** D2 › *Build agents that integrate retrieval*; *integrate agent tools, including … knowledge stores, search*. D5 › *Connect retrieval pipelines directly to workflows and agent tools*. D1 › *Choose appropriate memory, tool, and knowledge integration services*.

**You will learn**
- `AzureAISearchTool` + `AISearchIndexResource(project_connection_id, index_name, query_type, top_k, filter)`.
- Query types: `simple`, `semantic`, `vector`, `vector_simple_hybrid`, `vector_semantic_hybrid`.
- The project's managed identity reads the index (roles granted in `infra/core.bicep`). No search keys anywhere.

## Set up
Uses the shared `policies` index (auto-created). The project connection `search` comes from the platform template.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Resolve the connection ID; build the search tool (hybrid + semantic, top 4). | Connections decouple agents from endpoints and credentials. |
| 2 | A staff agent with `filter` restricting to `all-staff` documents. | Security trimming at query time. |
| 3 | Collect citations. | Grounding you can verify. |

## Run and test
```bash
./lab run 33 && ./lab validate 33      # one click: ./lab solve 33
```

## Explore
- **Foundry IQ**: create a *knowledge base* (portal → Knowledge) over this index plus SharePoint or the web. Agentic retrieval plans sub-queries across sources, and one knowledge base serves many agents.
- For per-user trimming in production, pass the signed-in user's groups into the filter (or use Search's document-level permissions).

## Exam reflexes
- Enterprise RAG for agents → **Azure AI Search tool** (or **Foundry IQ knowledge base** for multi-source, shared, agentic retrieval).
- Users must only see what they're allowed to → **security trimming** (filter on ACL fields / document-level permissions).

## Clean up
`./lab clean 33`
