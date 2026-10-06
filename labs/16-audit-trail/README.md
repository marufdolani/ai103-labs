# Lab 16 · Audit trail: traces, provenance, approvals

**Scenario.** Contoso's refund assistant can propose money movements. Internal audit requires: every AI decision traceable end to end, provenance metadata (which model, deployment, prompt version), a recorded human approval above USD 100, and evidence that logs weren't edited.

**Exam objectives.** D1 › *Implement auditing through trace logging, provenance metadata, and approval workflows*; *govern agent behaviour with oversight modes*. D2 › *Set up observability by implementing tracing*.

**You will learn**
- OpenTelemetry → Application Insights with `configure_azure_monitor()` + `OpenAIInstrumentor` (GenAI semantic conventions).
- Provenance metadata without storing sensitive text: hashes of prompts and system-prompt versions, response IDs, deployment names, content-filter annotations.
- A **hash-chained** audit log: tamper-evident by construction.
- Approval gates: auto-approve below a policy limit, require a human above it.

## Set up
App Insights is connected to the project (lab 01). Message content is **not** captured by default. Set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` only where policy allows.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Configure Azure Monitor from the project's connection string and instrument the OpenAI SDK. | Every model call becomes a span with tokens and latency. |
| 2 | `AuditLog.append()`: record event + trace/span IDs + previous hash, then hash the record. | Correlates audit records with traces; chains them. |
| 3 | `AuditLog.verify()`: recompute the chain. | Proves integrity; detects edits. |
| 4 | Approval policy: auto ≤ USD 100, otherwise request and record a human decision **before** executing. | Oversight mode for consequential actions. |

## Run and test
```bash
./lab run 16 && ./lab validate 16      # one click: ./lab solve 16
```
Search the printed trace ID in Application Insights → Transaction search (it appears after ~2 minutes).

## Explore
- Ship the audit JSONL to immutable storage (Blob with a time-based retention policy) for real WORM retention.
- C2PA content credentials are the provenance answer for **generated images** (lab 39).

## Exam reflexes
- "Trace every request end to end" → **OpenTelemetry tracing to Application Insights** connected to the project.
- "Human must approve consequential actions" → **approval workflow / human-in-the-loop** (MCP `require_approval`, lab 32; workflow approvals, lab 37).
- Provenance → model, deployment, response ID, prompt version, filter results (and C2PA for media).

## Clean up
Nothing to clean.
