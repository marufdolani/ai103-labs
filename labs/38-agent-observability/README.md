# Lab 38 · Agent tracing, evaluation and error analysis

**Scenario.** Contoso's order-status agent is live. Product wants to know: does it understand requests, stay in scope, and call the tool correctly? When it fails, why? You'll trace every run to Application Insights, score runs with agent evaluators, and build an error-analysis table.

**Exam objectives.** D2 › *Integrate monitoring into deployed agents, evaluate agent behaviour, and perform error analysis*; *set up observability by implementing tracing, token analytics, safety signals, and latency breakdowns*.

**You will learn**
- `AIProjectInstrumentor` + `configure_azure_monitor`: spans for agent runs, model calls and tool calls.
- Agent evaluators: **Intent Resolution**, **Task Adherence** (follows system instructions/scope), **Tool Call Accuracy** (right tool, right arguments). Each returns pass/fail with a reason.
- Turning evaluator reasons into a prioritized fix list.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Configure tracing to the project's Application Insights. | You can't fix what you can't see. |
| 2 | Score each case with the three agent evaluators. | Quality signals specific to agents. |
| 3 | Error analysis: failed evaluator + reason per case. | Tells you whether to fix instructions, tools or schemas. |

## Run and test
```bash
./lab run 38 && ./lab validate 38      # one click: ./lab solve 38
```
In the Foundry portal: **Tracing** shows each run; **Monitoring** shows agent dashboards once traffic flows.

## Explore
- Break the tool description (for example, "Get the weather") and watch Tool Call Accuracy fail with a clear reason.
- **Continuous evaluation**: `project().evaluation_rules` can score sampled production runs automatically. Pair it with alerts.

## Exam reflexes
- Did the agent understand the user → **Intent Resolution**. Follow its instructions/scope → **Task Adherence**. Right tool + arguments → **Tool Call Accuracy**. Finished the job → **Task Completion**.
- Observability = **traces (App Insights) + evaluations + metrics**.

## Clean up
`./lab clean 38`
