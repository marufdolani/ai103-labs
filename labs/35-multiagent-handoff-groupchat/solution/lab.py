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
    # >>> TODO 1: Triage hands off to billing or tech; stop once a specialist has answered
    triage = Agent(client, name="triage", instructions=(
        "You are the front desk. Do not answer questions yourself. Hand off billing/invoice/refund questions to "
        "billing and login/outage/bug questions to tech."))
    billing = Agent(client, name="billing", instructions="You are Contoso billing support. Resolve the issue in 3 sentences.")
    tech = Agent(client, name="tech", instructions="You are Contoso technical support. Give 3 troubleshooting steps.")

    def specialist_answered(conversation) -> bool:
        return any(getattr(m, "author_name", None) in SPECIALISTS and (m.text or "").strip() for m in conversation)

    workflow = (HandoffBuilder(participants=[triage, billing, tech])
                .with_start_agent(triage)
                .add_handoff(triage, [billing, tech])
                .with_autonomous_mode(agents=[triage], turn_limits={"triage": 2})
                .with_termination_condition(specialist_answered)
                .build())
    result = await workflow.run(question)
    # <<<
    return flatten(result.get_outputs() or result.get_intermediate_outputs())


async def group_chat() -> list[dict]:
    client = chat_client()
    # >>> TODO 2: Writer and critic refine a tagline; a manager agent picks speakers; max 4 rounds
    writer = Agent(client, name="writer", description="Writes and revises taglines",
                   instructions="Write or revise a tagline (max 8 words) for Contoso's AI helpdesk.")
    critic = Agent(client, name="critic", description="Critiques taglines",
                   instructions="Critique the latest tagline in one sentence: clarity, warmth, length.")
    manager = Agent(client, name="manager", instructions="Alternate between writer and critic. Finish after the writer's second revision.")
    workflow = GroupChatBuilder(participants=[writer, critic], orchestrator_agent=manager, max_rounds=4).build()
    result = await workflow.run("Create the tagline.")
    # <<<
    return flatten(result.get_outputs())


async def magentic() -> list[dict]:
    client = chat_client()
    # >>> TODO 3: Magentic: a manager plans and assigns work dynamically to a researcher and an analyst
    researcher = Agent(client, name="researcher", description="Knows Azure AI services and their purposes",
                       instructions="Provide factual information about Azure AI services when asked.")
    analyst = Agent(client, name="analyst", description="Builds comparisons and recommendations",
                    instructions="Turn facts into a concise comparison table and a recommendation.")
    manager = Agent(chat_client(cfg("LARGE_MODEL")), name="manager", instructions="You coordinate the team.")
    workflow = MagenticBuilder(participants=[researcher, analyst], manager_agent=manager, max_round_count=8).build()
    result = await workflow.run("Recommend Content Understanding or Document Intelligence for extracting fields from "
                                "varied supplier invoices that also arrive as photos. Give a 3-row comparison and a pick.")
    # <<<
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
