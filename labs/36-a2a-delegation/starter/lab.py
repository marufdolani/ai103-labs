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
    # TODO 1: Describe the remote agent with an AgentCard: name, description, JSON-RPC interface URL, skills
    raise NotImplementedError("TODO 1: Describe the remote agent with an AgentCard: name, description, JSON-RPC interface URL, skills  (see README step and solution/ if stuck)")


def serve() -> uvicorn.Server:
    card = build_card()
    # TODO 2: Wrap the Agent Framework agent in an A2AExecutor, add the agent-card and JSON-RPC routes, start uvicorn
    raise NotImplementedError("TODO 2: Wrap the Agent Framework agent in an A2AExecutor, add the agent-card and JSON-RPC routes, start uvicorn  (see README step and solution/ if stuck)")
    threading.Thread(target=server.run, daemon=True).start()
    for _ in range(50):
        if server.started:
            break
        time.sleep(0.2)
    return server


async def delegate() -> dict:
    # TODO 3: Discover the card, call the remote agent directly, then let a local orchestrator use it as a tool
    raise NotImplementedError("TODO 3: Discover the card, call the remote agent directly, then let a local orchestrator use it as a tool  (see README step and solution/ if stuck)")
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
