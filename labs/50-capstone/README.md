# Lab 50 · Capstone: governed, grounded knowledge agent

**Scenario.** Contoso is rolling out an internal policy assistant to 20,000 employees. Security, HR and the CIO each have conditions before go-live:
- **Security:** jailbreaks are stopped *before* they reach the model, and the agent can't take actions without a human.
- **HR:** staff never see restricted HR documents, even when they ask directly.
- **Audit:** every answer is traceable to a user, an agent version, a response ID, sources and approvals.
- **CIO:** release only if an automated quality gate passes.

You build all of it in one app, reusing patterns from labs 12, 16, 20, 33, 37 and 38.

**Exam objectives (cross-domain).** D1 › guardrails, auditing (trace logging, provenance, approval workflows), governing agent behaviour with tool-access controls, monitoring. D2 › agents with retrieval and function calling, safeguards and approvals, evaluation, observability. D5 › connect retrieval pipelines to agent tools, hybrid + semantic grounding.

## Architecture
```
user ─► Prompt Shields ──blocked──► audit
            │ ok
            ▼
   agent (per role, versioned) ── Azure AI Search tool (hybrid+semantic, group filter = security trimming)
            │ function_call: open_ticket
            ▼
   approval policy ──► execute or reject ──► result back to agent
            ▼
   answer + citations ─► audit.jsonl (user, role, agent@version, response id, trace id, citations, approvals)
            ▼
   quality gate: Groundedness (vs the role's visible context) + Intent Resolution ─► release yes/no
```

## Steps
| TODO | Build | Pattern from |
|---|---|---|
| 1 | Prompt Shields input guard | Lab 12 |
| 2 | Agent per role: AI Search tool with group filter + function tool | Labs 33, 30 |
| 3 | Approval policy for the action | Lab 37 |
| 4 | Approval-gated function-call loop | Labs 21, 37 |
| 5 | Append-only audit log with provenance | Lab 16 |
| 6 | Evaluation gate (groundedness + intent) | Labs 14, 26, 38 |

## Run and test
```bash
./lab run 50 && ./lab validate 50      # one click: ./lab solve 50
```
Then open `.out/lab50/audit.jsonl`, and in the Foundry portal → **Tracing**, find the `capstone.request` spans by trace ID.

## Stretch goals (exam-relevant)
- Attach a custom **guardrail** (lab 11) to the agent deployment and add **indirect attack** checks at the tool-response intervention point.
- Replace the static per-role agent with a **Foundry IQ knowledge base** shared by several agents (permission-aware retrieval).
- Run the gate in **GitHub Actions** (lab 07) and schedule **continuous evaluation** on production traffic (lab 10).
- Publish the agent to **Microsoft Teams / Microsoft 365 Copilot** from the Foundry portal.

## Exam reflexes
- Block attacks before inference → **Prompt Shields** on user input (and indirect attack detection on documents and tool output).
- Users must only see what they're entitled to → **security trimming** (filter on group IDs) or permission-aware knowledge sources.
- Agent takes consequential actions → **human approval** + least-privilege tools + **audit log** with provenance.
- Release decision → **evaluation gate** (groundedness, intent, task adherence) in CI/CD.

## Clean up
`./lab clean 50` deletes both agents. Run `azd down --purge` when you've finished all labs.
