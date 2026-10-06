"""Lab 32 - Agent with MCP tools: human approval and tool allow-lists."""
from azure.ai.projects.models import MCPTool, PromptAgentDefinition

from labkit import cfg, show
from labkit.agents import ask, delete_agent
from labkit.clients import openai, project

AGENT = "lab32-docs-agent"
MCP_URL = "https://learn.microsoft.com/api/mcp"
ALLOWED = ["microsoft_docs_search"]


def run_with_approvals(agent, question: str, decide) -> dict:
    """Run a question; every MCP call needs a decision from `decide(request) -> bool`."""
    conv = openai().conversations.create()
    decisions = []
    resp = ask(agent, question, conversation=conv.id)
    # >>> TODO 2: While the response contains mcp_approval_request items, decide and reply with mcp_approval_response items
    for _ in range(6):
        requests = [i for i in resp.output if i.type == "mcp_approval_request"]
        if not requests:
            break
        replies = []
        for req in requests:
            approved = bool(decide(req))
            decisions.append({"tool": req.name, "server": req.server_label, "args": req.arguments, "approved": approved})
            replies.append({"type": "mcp_approval_response", "approval_request_id": req.id, "approve": approved})
        resp = ask(agent, replies, conversation=conv.id)
    # <<<
    calls = [i.name for i in resp.output if i.type == "mcp_call"]
    openai().conversations.delete(conv.id)
    return {"answer": resp.output_text, "decisions": decisions, "mcp_calls_in_final": calls}


def reviewer_policy(req) -> bool:
    # >>> TODO 3: Approve only allow-listed tools whose arguments don't contain sensitive terms
    return req.name in ALLOWED and not any(word in (req.arguments or "").lower() for word in ("password", "secret", "key"))
    # <<<


def main() -> dict:
    delete_agent(AGENT)
    # >>> TODO 1: Agent with an MCPTool: server_label, server_url, require_approval='always', allowed_tools=ALLOWED
    agent = project().agents.create_version(
        agent_name=AGENT,
        definition=PromptAgentDefinition(
            model=cfg("CHAT_MODEL"),
            instructions="Answer Azure questions using the Microsoft Learn tools. Include one Learn link.",
            tools=[MCPTool(server_label="mslearn", server_url=MCP_URL, require_approval="always", allowed_tools=ALLOWED)],
        ),
    )
    # <<<
    q = "In Microsoft Foundry, what are the four guardrail intervention points? Answer briefly."
    approved = run_with_approvals(agent, q, reviewer_policy)
    denied = run_with_approvals(agent, q, lambda req: False)
    show.title("Approved run")
    show.table([[d["tool"], d["approved"], d["args"][:60]] for d in approved["decisions"]], ["tool", "approved", "arguments"])
    show.text("Answer", approved["answer"])
    show.title("Denied run")
    show.text("Answer", denied["answer"])
    return {"approved": approved, "denied": denied}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
