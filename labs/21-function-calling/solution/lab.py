"""Lab 21 - Function calling loop with the Responses API."""
import json

from labkit import cfg, show
from labkit.clients import openai

ORDERS = {
    "8812": {"status": "delivered", "carrier": "DHL", "total_usd": 300.0, "delivered": "2026-09-28"},
    "9901": {"status": "in transit", "carrier": "FedEx", "total_usd": 120.0, "eta": "2026-10-09"},
}


def get_order_status(order_id: str) -> dict:
    return ORDERS.get(order_id, {"error": f"order {order_id} not found"})


def calculate_refund(order_id: str, reason: str) -> dict:
    order = ORDERS.get(order_id)
    if not order:
        return {"error": "unknown order"}
    pct = 1.0 if reason == "damaged" else 0.5 if reason == "late" else 0.0
    return {"order_id": order_id, "refund_usd": round(order["total_usd"] * pct, 2), "policy": f"{int(pct * 100)}% for {reason}"}


FUNCTIONS = {"get_order_status": get_order_status, "calculate_refund": calculate_refund}

# Strict tool schemas: every property required and additionalProperties false.
TOOLS = [
    {"type": "function", "name": "get_order_status", "description": "Get shipping status for one order.", "strict": True,
     "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}},
                    "required": ["order_id"], "additionalProperties": False}},
    {"type": "function", "name": "calculate_refund", "description": "Calculate the refund for an order.", "strict": True,
     "parameters": {"type": "object",
                    "properties": {"order_id": {"type": "string"},
                                   "reason": {"type": "string", "enum": ["damaged", "late", "changed_mind"]}},
                    "required": ["order_id", "reason"], "additionalProperties": False}},
]


def run(question: str, max_rounds: int = 5) -> dict:
    calls_made = []
    # >>> TODO 1: First request with tools
    resp = openai().responses.create(model=cfg("CHAT_MODEL"), input=question, tools=TOOLS,
                                     instructions="Use the tools for order data. Never guess.",
                                     reasoning={"effort": "low"}, max_output_tokens=3000)
    # <<<
    rounds = 0
    while rounds < max_rounds:
        calls = [item for item in resp.output if item.type == "function_call"]
        if not calls:
            break
        rounds += 1
        # >>> TODO 2: Execute every call (they can arrive in parallel) and send function_call_output items back
        outputs = []
        for call in calls:
            args = json.loads(call.arguments)
            result = FUNCTIONS[call.name](**args)
            calls_made.append({"name": call.name, "args": args})
            outputs.append({"type": "function_call_output", "call_id": call.call_id, "output": json.dumps(result)})
        resp = openai().responses.create(model=cfg("CHAT_MODEL"), previous_response_id=resp.id, input=outputs,
                                         tools=TOOLS, reasoning={"effort": "low"}, max_output_tokens=3000)
        # <<<
    return {"answer": resp.output_text, "calls": calls_made, "rounds": rounds}


def main() -> dict:
    q = "Where are my orders 8812 and 9901? Order 8812 arrived damaged; how much will I get back?"
    out = run(q)
    show.table([[c["name"], json.dumps(c["args"])] for c in out["calls"]], ["function", "arguments"])
    show.text("Answer", out["answer"])
    return out


if __name__ == "__main__":
    show.result(main())
