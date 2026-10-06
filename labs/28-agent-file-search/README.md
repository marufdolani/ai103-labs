# Lab 28 · Agent with File Search

**Scenario.** A small Contoso team wants a policy Q&A agent this afternoon, without building an index pipeline. You'll upload the policy files to a managed **vector store**, attach **File Search** to an agent and check its citations.

**Exam objectives.** D2 › *Build agents that integrate retrieval*; *integrate agent tools, including … knowledge stores, search*. D1 › *Choose an appropriate method for retrieval and indexing*; *choose … knowledge integration services for agent solutions*.

**You will learn**
- Vector stores: managed chunking and embedding of uploaded files.
- `FileSearchTool(vector_store_ids=[...])`, `file_search_call` output items, `file_citation` annotations.
- When File Search is enough, and when you need Azure AI Search or Foundry IQ (lab 33).

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Create a vector store and upload the policies. | Zero-pipeline retrieval. |
| 2 | Agent with `FileSearchTool`. | Retrieval as a tool the agent decides to use. |
| 3 | Ask, then inspect tool calls and citations. | Verify grounding, don't assume it. |

## Run and test
```bash
./lab run 28 && ./lab validate 28      # one click: ./lab solve 28
./lab clean 28                         # deletes agent, vector store and files
```

## Exam reflexes
- "Search uploaded documents quickly, no index to build" → **File Search** (vector store).
- Enterprise scale, security trimming, hybrid/semantic ranking, many sources → **Azure AI Search tool / Foundry IQ**.

## Clean up
`./lab clean 28`
