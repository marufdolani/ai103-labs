# Lab 37 · Semi-autonomous workflow with safeguards

**Scenario.** Contoso's account-manager agent may issue service credits, which is real money. The agent works autonomously for lookups, but every credit needs a human decision. Hard limits apply no matter what the model or the approver says.

**Exam objectives.** D2 › *Build autonomous or semiautonomous workflows with safeguards and approval flow controls*. D1 › *Govern agent behaviour with oversight modes, constraints, and tool-access controls*.

**You will learn**
- Layered safeguards: **approval-gated tool** (`approval_mode="always_require"`), **invocation cap** (`max_invocations`), **hard limit in code**, and an honest report back to the user.
- The approval round-trip in Agent Framework: `response.user_input_requests` → `to_function_approval_response(approved)` → continue in the same session.
- Autonomy levels: read-only tools run freely; consequential tools pause for a human.

## Steps
| TODO | Build | Why |
|---|---|---|
| - | Read the `@tool(...)` decorator on `issue_credit`. | Safeguards declared where the capability lives. |
| 1 | `approver()`: approve ≤ USD 200 with a reason. | Human (or policy) decision on the actual arguments. |
| 2 | Approval loop within the session. | The agent resumes only after a decision. |

## Run and test
```bash
./lab run 37 && ./lab validate 37      # one click: ./lab solve 37
```

## Explore
- Route approvals to Teams or email with a Logic App, and persist pending requests (checkpointing) so a human can approve hours later.
- Foundry-hosted equivalent: MCP tools with `require_approval` (lab 32) and workflow agents with human-in-the-loop nodes.

## Exam reflexes
- Semi-autonomous = **autonomous for low-risk actions, approval for consequential ones**, plus limits enforced in code and full audit (lab 16).
- Never rely on the prompt alone to enforce a money limit.

## Clean up
Nothing to clean.
