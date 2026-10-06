"""Helpers for Foundry Agent Service labs (agents are versioned; invoked by agent_reference)."""
from __future__ import annotations

from azure.core.exceptions import ResourceNotFoundError

from .clients import credential, openai, project
from .config import cfg


def agent_reference(agent, pin_version: bool = True) -> dict:
    ref = {"name": agent.name, "type": "agent_reference"}
    if pin_version:
        ref["version"] = agent.version
    return {"agent_reference": ref}


def ask(agent, text_or_items, *, conversation: str | None = None, previous_response_id: str | None = None,
        pin_version: bool = True):
    """Send input to a Foundry agent and return the Responses API response."""
    kwargs = {}
    if conversation:
        kwargs["conversation"] = conversation
    if previous_response_id:
        kwargs["previous_response_id"] = previous_response_id
    return openai().responses.create(input=text_or_items, extra_body=agent_reference(agent, pin_version), **kwargs)


def delete_agent(name: str) -> None:
    try:
        project().agents.delete(name)
    except ResourceNotFoundError:
        pass


def citations(response) -> list[dict]:
    """Collect annotations (file, URL and container-file citations) from a response's message items."""
    found = []
    for item in response.output:
        if item.type != "message":
            continue
        for part in item.content:
            for ann in getattr(part, "annotations", None) or []:
                found.append({k: getattr(ann, k, None) for k in ("type", "filename", "file_id", "url", "title", "container_id")})
    return found


def chat_client(model: str | None = None):
    """Microsoft Agent Framework chat client backed by the Foundry project (keyless)."""
    from agent_framework.foundry import FoundryChatClient

    return FoundryChatClient(project_endpoint=cfg("PROJECT_ENDPOINT"), model=model or cfg("CHAT_MODEL"),
                             credential=credential())
