"""Lab 34 - Multi-agent orchestration with Microsoft Agent Framework: sequential and concurrent."""
import asyncio
import time

from agent_framework import Agent
from agent_framework.orchestrations import ConcurrentBuilder, SequentialBuilder

from labkit import show
from labkit.agents import chat_client
from labkit.workflows import assistant_turns, flatten

COMPLAINT = ("Customer Dana Ortiz (account 55-1209) was charged twice for her October subscription (USD 49 x2) "
             "and waited 6 days for a reply. She's threatening to cancel.")
CLAUSE = ("Supplier may process customer personal data in any country, retain it indefinitely, and limit its total "
          "liability to USD 1,000 regardless of the cause of loss. Payment terms: net 120 days.")


async def sequential() -> list[dict]:
    client = chat_client()
    # >>> TODO 1: Three agents (extractor -> drafter -> compliance reviewer) chained with SequentialBuilder
    extractor = Agent(client, name="extractor",
                      instructions="Extract the customer's name, account, issue and requested remedy as 4 short bullets.")
    drafter = Agent(client, name="drafter",
                    instructions="Using the bullets above, draft a short apology email offering a refund of the duplicate charge.")
    reviewer = Agent(client, name="reviewer",
                     instructions=("Review the draft above for compliance: no admissions of legal liability, refund amount "
                                   "correct, no personal data beyond the name. Start your reply with APPROVED or CHANGES:."))
    workflow = SequentialBuilder(participants=[extractor, drafter, reviewer]).build()
    result = await workflow.run(COMPLAINT)
    # <<<
    return flatten(result.get_outputs())


async def concurrent() -> list[dict]:
    client = chat_client()
    # >>> TODO 2: Three independent reviewers run in parallel with ConcurrentBuilder
    legal = Agent(client, name="legal", instructions="You are a contracts lawyer. List the top legal risk in one sentence.")
    finance = Agent(client, name="finance", instructions="You are a finance controller. List the top financial risk in one sentence.")
    privacy = Agent(client, name="privacy", instructions="You are a privacy officer. List the top data-protection risk in one sentence.")
    workflow = ConcurrentBuilder(participants=[legal, finance, privacy]).build()
    result = await workflow.run(f"Review this supplier clause:\n{CLAUSE}")
    # <<<
    return flatten(result.get_outputs())


def main() -> dict:
    t0 = time.perf_counter()
    seq = assistant_turns(asyncio.run(sequential()))
    t1 = time.perf_counter()
    con = assistant_turns(asyncio.run(concurrent()))
    t2 = time.perf_counter()
    show.title("Sequential")
    for r in seq:
        show.text(r["author"] or "agent", r["text"], limit=300)
    show.title("Concurrent")
    for r in con:
        show.text(r["author"] or "agent", r["text"], limit=300)
    show.kv({"sequential seconds": round(t1 - t0, 1), "concurrent seconds": round(t2 - t1, 1)})
    return {"sequential": seq, "concurrent": con}


if __name__ == "__main__":
    show.result(main())
