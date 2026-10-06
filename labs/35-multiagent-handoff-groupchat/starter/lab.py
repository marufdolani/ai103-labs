"""Lab 35 - Multi-agent orchestration: handoff, group chat and Magentic."""
import asyncio

from agent_framework import Agent
from agent_framework.orchestrations import GroupChatBuilder, HandoffBuilder, MagenticBuilder

from labkit import cfg, show
from labkit.agents import chat_client
from labkit.workflows import assistant_turns, flatten

SPECIALISTS = {"billing", "tech"}


async def handoff(question: str) -> list[dict]:
    client = chat_client()
    # TODO 1: Triage hands off to billing or tech; stop once a specialist has answered
    raise NotImplementedError("TODO 1: Triage hands off to billing or tech; stop once a specialist has answered  (see README step and solution/ if stuck)")
    return flatten(result.get_outputs() or result.get_intermediate_outputs())


async def group_chat() -> list[dict]:
    client = chat_client()
    # TODO 2: Writer and critic refine a tagline; a manager agent picks speakers; max 4 rounds
    raise NotImplementedError("TODO 2: Writer and critic refine a tagline; a manager agent picks speakers; max 4 rounds  (see README step and solution/ if stuck)")
    return flatten(result.get_outputs())


async def magentic() -> list[dict]:
    client = chat_client()
    # TODO 3: Magentic: a manager plans and assigns work dynamically to a researcher and an analyst
    raise NotImplementedError("TODO 3: Magentic: a manager plans and assigns work dynamically to a researcher and an analyst  (see README step and solution/ if stuck)")
    return flatten(result.get_outputs())


def main() -> dict:
    billing_case = assistant_turns(asyncio.run(handoff("I was charged twice for my subscription this month.")))
    tech_case = assistant_turns(asyncio.run(handoff("I can't sign in, the page says error AADSTS50076.")))
    chat = assistant_turns(asyncio.run(group_chat()))
    mag = assistant_turns(asyncio.run(magentic()))
    show.title("Handoff")
    show.kv({"billing question answered by": [r["author"] for r in billing_case],
             "tech question answered by": [r["author"] for r in tech_case]})
    show.title("Group chat")
    for r in chat:
        show.text(r["author"], r["text"], limit=200)
    show.title("Magentic final answer")
    show.text("answer", mag[-1]["text"] if mag else "", limit=1200)
    return {"billing_case": billing_case, "tech_case": tech_case, "group_chat": chat, "magentic": mag}


if __name__ == "__main__":
    show.result(main())
