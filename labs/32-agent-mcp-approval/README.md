# Lab 32 · Agent with MCP: approvals and allow-lists

**Scenario.** Contoso wants agents to use tools published over the **Model Context Protocol** (here, the public Microsoft Learn MCP server). Governance requires that the agent can only reach approved tools, and that a reviewer approves each call before it runs.

**Exam objectives.** D2 › *Integrate agent tools*; *build autonomous or semiautonomous workflows with safeguards and approval flow controls*. D1 › *Govern agent behaviour with oversight modes, constraints, and tool-access controls*.

**You will learn**
- `MCPTool(server_label, server_url, require_approval, allowed_tools, project_connection_id)`.
- The approval protocol: `mcp_approval_request` (tool + arguments) → your decision → `mcp_approval_response`.
- Allow-lists shrink the attack surface: the model never sees tools you didn't allow.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Agent with an MCP tool, `require_approval="always"`, `allowed_tools`. | Oversight mode + least privilege. |
| 2 | Approval loop: answer every `mcp_approval_request`. | Human-in-the-loop at the protocol level. |
| 3 | Reviewer policy: allow-listed tools, no sensitive terms in arguments. | Automate the easy decisions; escalate the rest. |

## Run and test
```bash
./lab run 32 && ./lab validate 32      # one click: ./lab solve 32
```

## Explore
- Authenticated MCP servers: store the key or OAuth details in a **project connection** and pass `project_connection_id`.
- `require_approval` also accepts per-tool rules (`MCPToolRequireApproval`): "never" for read-only tools, "always" for writes.
- Guardrails can scan **tool call** and **tool response** intervention points too (lab 11).

## Exam reflexes
- "Human must approve each sensitive tool call" → **`require_approval="always"`** + approval responses.
- "Restrict which tools an agent may call" → **`allowed_tools`** + least-privilege connection identity.
- MCP = **agent ↔ tool** protocol. A2A = **agent ↔ agent** (lab 36).

## Clean up
`./lab clean 32`
