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
    # TODO 1: Three agents (extractor -> drafter -> compliance reviewer) chained with SequentialBuilder
    raise NotImplementedError("TODO 1: Three agents (extractor -> drafter -> compliance reviewer) chained with SequentialBuilder  (see README step and solution/ if stuck)")
    return flatten(result.get_outputs())


async def concurrent() -> list[dict]:
    client = chat_client()
    # TODO 2: Three independent reviewers run in parallel with ConcurrentBuilder
    raise NotImplementedError("TODO 2: Three independent reviewers run in parallel with ConcurrentBuilder  (see README step and solution/ if stuck)")
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
