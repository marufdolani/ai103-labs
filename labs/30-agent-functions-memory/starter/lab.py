"""Lab 30 - Agent with custom functions and memory (short-term + long-term)."""
import json

from azure.ai.projects.models import FunctionTool, PromptAgentDefinition

from labkit import cfg, out_path, show
from labkit.agents import ask, delete_agent
from labkit.clients import openai, project

AGENT = "lab30-hr-memory"
MEMORY_FILE = out_path("lab30", "memory.json")
LEAVE = {"E-1001": {"annual_days_left": 14, "family_care_days_left": 6}}


def _memory() -> dict:
    return json.loads(MEMORY_FILE.read_text()) if MEMORY_FILE.exists() else {}


def get_leave_balance(employee_id: str) -> dict:
    return LEAVE.get(employee_id, {"error": "unknown employee"})


def remember_preference(employee_id: str, key: str, value: str) -> dict:
    mem = _memory()
    mem.setdefault(employee_id, {})[key] = value
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))
    return {"saved": True}


def recall_preferences(employee_id: str) -> dict:
    return _memory().get(employee_id, {})


FUNCS = {f.__name__: f for f in (get_leave_balance, remember_preference, recall_preferences)}


def schema(**props) -> dict:
    return {"type": "object", "properties": {k: {"type": "string"} for k in props},
            "required": list(props), "additionalProperties": False}


def run_turn(agent, conversation_id: str, text: str, log: list) -> str:
    resp = ask(agent, text, conversation=conversation_id)
    # TODO 2: Execute function calls the agent requests and send outputs back in the SAME conversation (max 5 rounds)
    raise NotImplementedError("TODO 2: Execute function calls the agent requests and send outputs back in the SAME conversation (max 5 rounds)  (see README step and solution/ if stuck)")
    return resp.output_text


def main() -> dict:
    delete_agent(AGENT)
    MEMORY_FILE.write_text("{}")
    # TODO 1: Agent with three FunctionTools and instructions that make it recall preferences at the start of each conversation
    raise NotImplementedError("TODO 1: Agent with three FunctionTools and instructions that make it recall preferences at the start of each conversation  (see README step and solution/ if stuck)")
    calls: list[str] = []
    conv1 = openai().conversations.create()
    a1 = run_turn(agent, conv1.id, "I'm employee E-1001. Please call me Sam from now on. How many annual leave days do I have?", calls)
    show.text("Conversation 1", a1)

    # TODO 3: Start a NEW conversation (no shared history) and ask again; long-term memory must carry the name
    raise NotImplementedError("TODO 3: Start a NEW conversation (no shared history) and ask again; long-term memory must carry the name  (see README step and solution/ if stuck)")
    show.text("Conversation 2 (new)", a2)
    show.kv({"function calls": calls, "memory": _memory()})
    for c in (conv1, conv2):
        openai().conversations.delete(c.id)
    return {"answer1": a1, "answer2": a2, "calls": calls, "memory": _memory()}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
