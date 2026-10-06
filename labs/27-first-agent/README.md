# Lab 27 · First prompt agent with versions

**Scenario.** Contoso HR wants a helpdesk agent that every team can call by name, with controlled changes: a new behaviour ships as a new **version**, and callers can pin to a version they've tested.

**Exam objectives.** D2 › Build agents by using Foundry: *define agent roles, goals, conversation-tracking approach*. D1 › *Configure model and agent deployments*.

**You will learn**
- Agent kinds: **prompt** agents (declarative: model + instructions + tools), **workflow** agents, **hosted** agents (your code in a container).
- `project.agents.create_version(agent_name, definition=PromptAgentDefinition(...))`: every change creates an immutable version.
- Invoking: `openai.responses.create(..., extra_body={"agent_reference": {"name", "version", "type"}})` inside a **conversation**.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Version 1 with role, goal, boundaries + metadata. | Good instructions state role, goal and limits. |
| 2 | Conversation with two turns. | Conversation = server-side memory for the agent. |
| 3 | Version 2 with different behaviour. | Same name, new version. |
| 4 | List versions. | Release management and rollback. |

## Run and test
```bash
./lab run 27 && ./lab validate 27      # one click: ./lab solve 27
./lab clean 27
```

## Explore
- Open the Foundry portal → Agents: try both versions in the playground and view each conversation.
- Omit `version` in the agent reference to always call the latest.

## Exam reflexes
- Classic → new: **threads → conversations**, **runs → responses**, assistants → **versioned agents** (`create_version` + `agent_reference`).
- Declarative agent → **prompt agent**. Multi-agent declarative flow → **workflow agent**. Your own framework code → **hosted agent**.

## Clean up
`./lab clean 27`
