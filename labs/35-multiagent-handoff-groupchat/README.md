# Lab 35 · Multi-agent: handoff, group chat, Magentic

**Scenario.** Contoso's support front door must route customers to the right specialist, who then owns the conversation (handoff). Marketing wants agents to iterate on copy together (group chat). Architecture wants a team that plans its own work on open-ended questions (Magentic).

**Exam objectives.** D2 › *Implement orchestrated multi-agent solutions*; *build autonomous or semiautonomous workflows with safeguards*.

**You will learn**
- **Handoff**: triage transfers control; termination conditions and autonomous turn limits are your safeguards.
- **Group chat**: a manager (orchestrator agent) selects the next speaker; `max_rounds` bounds cost.
- **Magentic**: the manager keeps a task/progress ledger, plans, assigns and re-plans; `max_round_count` bounds it.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Handoff workflow (start agent, handoff targets, autonomous triage, termination). | Routing + ownership transfer. |
| 2 | Group chat with a manager and `max_rounds`. | Iterative collaboration. |
| 3 | Magentic with a manager on the large model. | Dynamic planning for open-ended tasks. |

## Run and test
```bash
./lab run 35 && ./lab validate 35      # one click: ./lab solve 35
```
Magentic makes many calls; expect a few minutes.

## Explore
- Remove `with_autonomous_mode`: the workflow pauses to ask the user after the triage reply. That's human-in-the-loop by default.
- `MagenticBuilder(..., enable_plan_review=True)` asks a human to approve the plan before execution.

## Exam reflexes
- Specialist must **take over** → handoff. Agents **refine one output together** → group chat. **Open-ended task, dynamic plan** → Magentic. Known stages → sequential. Independent parallel work → concurrent.
- Bound every multi-agent loop: max rounds, termination conditions, plan review.

## Clean up
Nothing to clean.
