"""Lab 38 - Agent tracing, evaluation and error analysis."""
import json

from azure.ai.evaluation import IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

from labkit import cfg, show
from labkit.agents import ask, delete_agent
from labkit.clients import openai, project
from labkit.evals import REASONING_JUDGE, judge_config

AGENT = "lab38-order-agent"
INSTRUCTIONS = ("You are Contoso's order-status agent. Only answer questions about order status using get_order_status. "
                "Politely decline anything else (bookings, advice, other topics).")
ORDERS = {"8812": "delivered on 28 Sep", "9901": "in transit, ETA 9 Oct", "7710": "cancelled by customer"}
TOOL_DEF = {"name": "get_order_status", "description": "Get the shipping status of an order",
            "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}},
                           "required": ["order_id"], "additionalProperties": False}}
CASES = [
    "Where is order 9901?",
    "What happened to orders 7710 and 8812?",
    "Can you book me a flight to Tokyo next week?",
]


def run_case(agent, question: str, tracer) -> dict:
    with tracer.start_as_current_span(f"case: {question[:40]}") as span:
        conv = openai().conversations.create()
        resp = ask(agent, question, conversation=conv.id)
        tool_calls = []
        for _ in range(4):
            calls = [i for i in resp.output if i.type == "function_call"]
            if not calls:
                break
            outputs = []
            for c in calls:
                args = json.loads(c.arguments)
                tool_calls.append({"type": "tool_call", "tool_call_id": c.call_id, "name": c.name, "arguments": args})
                outputs.append({"type": "function_call_output", "call_id": c.call_id,
                                "output": json.dumps({"status": ORDERS.get(args["order_id"], "unknown order")})})
            resp = ask(agent, outputs, conversation=conv.id)
        openai().conversations.delete(conv.id)
        return {"query": question, "response": resp.output_text, "tool_calls": tool_calls,
                "trace_id": f"{span.get_span_context().trace_id:032x}"}


def evaluate_case(case: dict) -> dict:
    judge = judge_config()
    # >>> TODO 2: Score intent resolution, task adherence and (when tools were called) tool call accuracy
    scores = {
        "intent_resolution": IntentResolutionEvaluator(judge, **REASONING_JUDGE)(query=case["query"], response=case["response"]),
        "task_adherence": TaskAdherenceEvaluator(judge, **REASONING_JUDGE)(
            query=[{"role": "system", "content": INSTRUCTIONS}, {"role": "user", "content": case["query"]}],
            response=case["response"]),
    }
    if case["tool_calls"]:
        scores["tool_call_accuracy"] = ToolCallAccuracyEvaluator(judge, **REASONING_JUDGE)(
            query=case["query"], tool_calls=case["tool_calls"], tool_definitions=[TOOL_DEF])
    # <<<
    return scores


def error_analysis(cases: list[dict]) -> list[dict]:
    # >>> TODO 3: List every failed evaluator per case with its reason, so you know what to fix
    failures = []
    for case in cases:
        for name, out in case["scores"].items():
            if str(out.get(f"{name}_result", "pass")).lower() == "fail":
                failures.append({"query": case["query"], "evaluator": name, "reason": str(out.get(f"{name}_reason", ""))[:200]})
    return failures
    # <<<


def main() -> dict:
    # >>> TODO 1: Tracing: Azure Monitor exporter from the project + Foundry/agent instrumentation
    configure_azure_monitor(connection_string=project().telemetry.get_application_insights_connection_string())
    from azure.ai.projects.telemetry import AIProjectInstrumentor
    AIProjectInstrumentor().instrument()
    # <<<
    tracer = trace.get_tracer("ai103.lab38")
    delete_agent(AGENT)
    agent = project().agents.create_version(agent_name=AGENT, definition=PromptAgentDefinition(
        model=cfg("CHAT_MODEL"), instructions=INSTRUCTIONS,
        tools=[FunctionTool(name=TOOL_DEF["name"], description=TOOL_DEF["description"],
                            parameters=TOOL_DEF["parameters"], strict=True)]))

    cases = [run_case(agent, q, tracer) for q in CASES]
    for case in cases:
        case["scores"] = evaluate_case(case)
    trace.get_tracer_provider().force_flush()

    show.table([[c["query"][:40], len(c["tool_calls"]),
                 *(c["scores"].get(k, {}).get(f"{k}_result", "-") for k in ("intent_resolution", "task_adherence", "tool_call_accuracy")),
                 c["trace_id"][:12]] for c in cases],
               ["case", "tools", "intent", "adherence", "tool acc.", "trace"])
    failures = error_analysis(cases)
    show.title("Error analysis")
    show.table([[f["query"][:40], f["evaluator"], f["reason"][:80]] for f in failures] or [["(no failures)", "", ""]],
               ["case", "evaluator", "reason"])
    return {"cases": cases, "failures": failures}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
