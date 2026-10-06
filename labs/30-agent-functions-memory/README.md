# Lab 30 · Agent with custom functions and memory

**Scenario.** Contoso's HR agent should look up live leave balances and remember lasting preferences, such as the name someone wants to be called, across separate conversations days apart.

**Exam objectives.** D2 › *Build agents that integrate retrieval, function-calling, and conversation memory*; *define … tool schemas*. D1 › *Choose appropriate memory, tool, and knowledge integration services for agent solutions*.

**You will learn**
- `FunctionTool` on a prompt agent: the service asks, **your app executes**, results return as `function_call_output` in the same conversation.
- Two kinds of memory: **short-term** (the conversation's items) and **long-term** (facts persisted outside the conversation and recalled by a tool).
- Writing instructions that make the agent use memory tools reliably.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Agent with three strict `FunctionTool`s and memory-aware instructions. | Tool schemas are the agent's API contract. |
| 2 | Execute function calls within the conversation loop. | Same pattern as lab 21, but agent-hosted. |
| 3 | New conversation: prove long-term memory works without shared history. | Memory ≠ chat history. |

## Run and test
```bash
./lab run 30 && ./lab validate 30      # one click: ./lab solve 30
```

## Explore
- Foundry offers a managed **memory store** (preview: `MemorySearchPreviewTool` + `project.beta.memory_stores`) that extracts and recalls user memories for you. Compare it with this explicit design.
- Store memories in Cosmos DB instead of a local file. Keep the same tool contract.

## Exam reflexes
- Multi-turn context → **conversation** (short-term). Facts across sessions → **long-term memory store** (managed memory or your own store behind a tool).
- Function tools: the agent decides; your code executes and enforces business rules.

## Clean up
`./lab clean 30`
