# Lab 36 · Agent-to-agent (A2A) discovery and delegation

**Scenario.** Contoso's finance team owns a travel-policy agent; the travel team builds a trip planner on a different stack. Instead of copying rules, the planner should **discover** the finance agent and **delegate** policy questions to it over the open **A2A** protocol.

**Exam objectives.** D2 › *Implement orchestrated multi-agent solutions*; *integrate agent tools*.

**You will learn**
- The **agent card** (`/.well-known/agent-card.json`): name, description, skills, interfaces, so other agents can discover capabilities.
- Exposing an Agent Framework agent over A2A (`A2AExecutor` + A2A server routes).
- Consuming a remote agent (`A2AAgent`) directly or **as a tool** of another agent.

## Set up
Everything runs locally: the remote agent listens on `127.0.0.1:9871` in a background thread and uses your Foundry model.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Build the `AgentCard` (interface URL, skills, examples). | Discovery contract. |
| 2 | Serve the agent: executor, card route, JSON-RPC route. | Any A2A client on any framework can now call it. |
| 3 | Discover, call directly, then delegate via `as_tool()`. | Agent-to-agent composition. |

## Run and test
```bash
./lab run 36 && ./lab validate 36      # one click: ./lab solve 36
```

## Explore
- Foundry prompt agents can call remote A2A agents with `A2APreviewTool(base_url=..., project_connection_id=...)` once the remote agent has a reachable URL (for example, hosted in Azure Container Apps).
- Add authentication: A2A cards declare `security_schemes`; clients send tokens accordingly.

## Exam reflexes
- "Agents built on different frameworks/vendors discover each other and delegate tasks" → **A2A** (agent cards).
- "Agent uses external tools via a standard protocol" → **MCP**.

## Clean up
Nothing to clean; the local server stops when the lab ends.
