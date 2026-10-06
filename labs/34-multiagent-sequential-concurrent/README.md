# Lab 34 · Multi-agent: sequential and concurrent

**Scenario.** Two Contoso processes need several specialists. (1) Complaint handling is a pipeline: extract facts → draft a reply → compliance review. (2) Supplier-contract triage needs independent legal, finance and privacy opinions as fast as possible.

**Exam objectives.** D2 › *Implement orchestrated multi-agent solutions*; *design workflows*.

**You will learn**
- Microsoft Agent Framework (successor to Semantic Kernel agents + AutoGen): `Agent(client, name, instructions)` with a `FoundryChatClient`.
- **Sequential** orchestration: each agent sees the conversation so far and adds to it.
- **Concurrent** orchestration: fan-out to independent agents, fan-in of results (optionally with a custom aggregator).

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Extractor → drafter → reviewer with `SequentialBuilder`. | Stages with dependencies. |
| 2 | Legal, finance, privacy with `ConcurrentBuilder`. | Independent work in parallel; lower wall-clock time. |

## Run and test
```bash
./lab run 34 && ./lab validate 34      # one click: ./lab solve 34
```

## Explore
- `ConcurrentBuilder(...).with_aggregator(fn)`: merge the three opinions into one risk rating with another agent.
- The same patterns exist declaratively as Foundry **workflow agents** (portal → Workflows). Compare the visual designer with this code.

## Exam reflexes
- Fixed stages, each needs the previous output → **sequential**. Independent analyses, merge results → **concurrent**.
- Triage then specialist takes over → **handoff**. Debate/refine with a manager → **group chat**. Open-ended planning → **Magentic** (lab 35).

## Clean up
Nothing to clean (Agent Framework agents here are in-process).
