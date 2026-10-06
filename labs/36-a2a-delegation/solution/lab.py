"""Lab 36 - Agent-to-agent (A2A): expose an agent, discover it by its agent card, delegate to it."""
import asyncio
import threading
import time

import httpx
import uvicorn
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import add_a2a_routes_to_fastapi, create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from agent_framework import Agent
from agent_framework.a2a import A2AAgent, A2AExecutor
from fastapi import FastAPI

from labkit import show
from labkit.agents import chat_client

HOST, PORT = "127.0.0.1", 9871
BASE_URL = f"http://{HOST}:{PORT}"


def travel_policy_agent() -> Agent:
    return Agent(chat_client(), name="travel-policy", instructions=(
        "You are Contoso's travel-policy expert. Rules: economy for flights under 6 hours; business class for 6+ hours "
        "with director approval; hotel cap USD 250/night in New York, London, Tokyo, Sydney, USD 180 elsewhere; "
        "meals USD 75/day. Answer in 2 sentences."))


def build_card() -> AgentCard:
    # >>> TODO 1: Describe the remote agent with an AgentCard: name, description, JSON-RPC interface URL, skills
    return AgentCard(
        name="Contoso travel-policy agent",
        description="Answers questions about Contoso travel and expense rules.",
        version="1.0.0",
        supported_interfaces=[AgentInterface(url=f"{BASE_URL}/a2a", protocol_binding="JSONRPC")],
        capabilities=AgentCapabilities(streaming=False),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[AgentSkill(id="travel-policy", name="Travel policy", tags=["travel", "expenses"],
                           description="Flight class, hotel caps and meal allowances",
                           examples=["Can I fly business class to Tokyo?"])],
    )
    # <<<


def serve() -> uvicorn.Server:
    card = build_card()
    # >>> TODO 2: Wrap the Agent Framework agent in an A2AExecutor, add the agent-card and JSON-RPC routes, start uvicorn
    handler = DefaultRequestHandler(agent_executor=A2AExecutor(travel_policy_agent()), task_store=InMemoryTaskStore(),
                                    agent_card=card)
    app = FastAPI()
    add_a2a_routes_to_fastapi(app, agent_card_routes=create_agent_card_routes(card),
                              jsonrpc_routes=create_jsonrpc_routes(handler, rpc_url="/a2a"))
    server = uvicorn.Server(uvicorn.Config(app, host=HOST, port=PORT, log_level="warning"))
    # <<<
    threading.Thread(target=server.run, daemon=True).start()
    for _ in range(50):
        if server.started:
            break
        time.sleep(0.2)
    return server


async def delegate() -> dict:
    # >>> TODO 3: Discover the card, call the remote agent directly, then let a local orchestrator use it as a tool
    card = httpx.get(f"{BASE_URL}/.well-known/agent-card.json", timeout=10).json()
    remote = A2AAgent(name="travel_policy", url=BASE_URL)
    direct = await remote.run("Can I fly business class from Sydney to Melbourne (1.5 hours)?")
    planner = Agent(chat_client(), name="trip-planner",
                    instructions="Plan business trips. Always check travel policy with the travel_policy tool before advising.",
                    tools=[remote.as_tool(name="travel_policy", description="Ask Contoso's travel-policy agent")])
    plan = await planner.run("I'm going to Tokyo for 3 nights. Which flight class and what hotel budget can I book from Sydney (9.5 hours)?")
    # <<<
    return {"card_name": card.get("name"), "skills": [s.get("id") for s in card.get("skills", [])],
            "direct": direct.text, "plan": plan.text}


def main() -> dict:
    server = serve()
    try:
        out = asyncio.run(delegate())
    finally:
        server.should_exit = True
    show.kv({"discovered": out["card_name"], "skills": out["skills"]})
    show.text("Direct A2A call", out["direct"])
    show.text("Orchestrator using the remote agent", out["plan"])
    return out


if __name__ == "__main__":
    show.result(main())
