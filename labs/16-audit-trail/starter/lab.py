"""Lab 16 - Audit trail: OpenTelemetry traces, provenance metadata, approval records."""
import hashlib
import json
import time
from pathlib import Path

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor

from labkit import cfg, out_path, show
from labkit.clients import aoai, project

SYSTEM_PROMPT = "You are Contoso's refund assistant. Propose refunds by calling propose_refund. Never invent order data."
REFUND_TOOL = {
    "type": "function",
    "function": {
        "name": "propose_refund",
        "description": "Propose a refund for an order",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}, "amount_usd": {"type": "number"}},
                       "required": ["order_id", "amount_usd"]},
    },
}
AUTO_APPROVE_LIMIT_USD = 100


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class AuditLog:
    """Append-only, hash-chained JSONL log: editing any past record breaks the chain."""

    def __init__(self, path: Path):
        self.path = path
        path.write_text("", encoding="utf-8")
        self.last_hash = "0" * 64

    def append(self, event: str, **data) -> dict:
        span = trace.get_current_span().get_span_context()
        # TODO 2: Build the record (event, time, trace/span IDs, data, prev hash), hash it, append as JSON
        raise NotImplementedError("TODO 2: Build the record (event, time, trace/span IDs, data, prev hash), hash it, append as JSON  (see README step and solution/ if stuck)")
        trace.get_current_span().add_event(event, {k: str(v) for k, v in data.items()})
        return record

    @staticmethod
    def verify(lines: list[str]) -> bool:
        # TODO 3: Recompute each hash and check every record points at the previous one
        raise NotImplementedError("TODO 3: Recompute each hash and check every record points at the previous one  (see README step and solution/ if stuck)")


def main() -> dict:
    # TODO 1: Send traces to the project's Application Insights and auto-instrument the OpenAI SDK
    raise NotImplementedError("TODO 1: Send traces to the project's Application Insights and auto-instrument the OpenAI SDK  (see README step and solution/ if stuck)")
    tracer = trace.get_tracer("ai103.lab16")
    log = AuditLog(out_path("lab16", "audit.jsonl"))
    user_request = "Customer says order 8812 arrived broken. Please refund the full USD 300."

    with tracer.start_as_current_span("refund-request") as span:
        trace_id = f"{span.get_span_context().trace_id:032x}"
        log.append("request_received", user=sha256("employee-4711")[:16], prompt_sha256=sha256(user_request),
                   system_prompt_version=sha256(SYSTEM_PROMPT)[:12])

        resp = aoai().chat.completions.create(
            model=cfg("CHAT_MODEL"),
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_request}],
            tools=[REFUND_TOOL], tool_choice="required", max_completion_tokens=1500)
        call = resp.choices[0].message.tool_calls[0]
        args = json.loads(call.function.arguments)
        filters = (resp.model_extra or {}).get("prompt_filter_results", [])
        log.append("model_proposed_action", response_id=resp.id, model=resp.model, deployment=cfg("CHAT_MODEL"),
                   tool=call.function.name, args=args, content_filter=json.dumps(filters)[:500])

        # TODO 4: Approval workflow: auto-approve under the limit, otherwise record a human decision before acting
        raise NotImplementedError("TODO 4: Approval workflow: auto-approve under the limit, otherwise record a human decision before acting  (see README step and solution/ if stuck)")

    trace.get_tracer_provider().force_flush()
    lines = log.path.read_text(encoding="utf-8").splitlines()
    tampered = list(lines)
    rec = json.loads(tampered[-1])
    rec["data"]["amount_usd"] = 3000
    tampered[-1] = json.dumps(rec, sort_keys=True)

    show.table([[json.loads(l)["event"], json.loads(l)["hash"][:12]] for l in lines], ["event", "hash"])
    show.kv({"trace_id (search it in App Insights > Transaction search)": trace_id})
    return {
        "trace_id": trace_id,
        "events": [json.loads(l)["event"] for l in lines],
        "chain_valid": AuditLog.verify(lines),
        "tamper_detected": not AuditLog.verify(tampered),
        "proposed_amount": args["amount_usd"],
    }


if __name__ == "__main__":
    show.result(main())
