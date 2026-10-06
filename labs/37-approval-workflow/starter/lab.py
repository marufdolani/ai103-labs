"""Lab 37 - Semi-autonomous workflow with safeguards: approval-gated tools, limits, audit."""
import asyncio
import json

from agent_framework import Agent, Message, tool

from labkit import show
from labkit.agents import chat_client

ACCOUNTS = {"ACME-77": {"credit_usd": 0.0, "plan": "Business"}}
LEDGER: list[dict] = []
MAX_CREDIT_USD = 500


@tool(description="Look up a customer account")
def get_account(account_id: str) -> str:
    return json.dumps(ACCOUNTS.get(account_id, {"error": "not found"}))


# Safeguards on the tool itself: approval_mode forces a human decision; max_invocations caps calls per run.
@tool(description="Issue a service credit in USD to a customer account", approval_mode="always_require", max_invocations=2)
def issue_credit(account_id: str, amount_usd: float, reason: str) -> str:
    if amount_usd > MAX_CREDIT_USD:  # hard limit enforced in code, whatever the model or approver says
        return json.dumps({"error": f"credits above USD {MAX_CREDIT_USD} need a finance ticket"})
    ACCOUNTS[account_id]["credit_usd"] += amount_usd
    LEDGER.append({"account": account_id, "amount": amount_usd, "reason": reason})
    return json.dumps({"ok": True, "new_credit_usd": ACCOUNTS[account_id]["credit_usd"]})


def approver(function_call) -> bool:
    """The human (simulated): approve credits up to USD 200 with a reason; reject the rest."""
    # TODO 1: Decide based on the requested arguments
    raise NotImplementedError("TODO 1: Decide based on the requested arguments  (see README step and solution/ if stuck)")


async def handle(request_text: str) -> dict:
    agent = Agent(chat_client(), name="account-manager", tools=[get_account, issue_credit], instructions=(
        "You manage customer accounts. Check the account first. Issue service credits when justified, using the "
        "amount the user asks for. Report the outcome honestly, including rejections."))
    session = agent.create_session()
    decisions = []
    response = await agent.run(request_text, session=session)
    # TODO 2: While the response has user_input_requests, ask the approver and send approval responses back
    raise NotImplementedError("TODO 2: While the response has user_input_requests, ask the approver and send approval responses back  (see README step and solution/ if stuck)")
    return {"answer": response.text, "decisions": decisions}


def main() -> dict:
    small = asyncio.run(handle("ACME-77 had a 3-hour outage. Please give them a USD 150 credit for the outage."))
    large = asyncio.run(handle("ACME-77 is unhappy. Give them a USD 450 credit as goodwill."))
    show.title("USD 150 request")
    show.kv({"decisions": small["decisions"]})
    show.text("Agent", small["answer"])
    show.title("USD 450 request")
    show.kv({"decisions": large["decisions"]})
    show.text("Agent", large["answer"])
    show.kv({"ledger": LEDGER, "account": ACCOUNTS["ACME-77"]})
    return {"small": small, "large": large, "ledger": LEDGER, "credit": ACCOUNTS["ACME-77"]["credit_usd"]}


if __name__ == "__main__":
    show.result(main())
