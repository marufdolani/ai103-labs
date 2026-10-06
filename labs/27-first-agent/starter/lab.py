"""Lab 27 - First prompt agent with versions."""
from azure.ai.projects.models import PromptAgentDefinition

from labkit import cfg, show
from labkit.agents import ask, delete_agent
from labkit.clients import openai, project

AGENT = "lab27-hr-helpdesk"


def main() -> dict:
    delete_agent(AGENT)

    show.step("Version 1")
    # TODO 1: Create version 1: role, goal and boundaries in the instructions
    raise NotImplementedError("TODO 1: Create version 1: role, goal and boundaries in the instructions  (see README step and solution/ if stuck)")
    show.kv({"name": v1.name, "version": v1.version, "id": v1.id})

    show.step("Conversation with v1")
    # TODO 2: Create a conversation and ask two related questions with the agent reference
    raise NotImplementedError("TODO 2: Create a conversation and ask two related questions with the agent reference  (see README step and solution/ if stuck)")
    show.text("v1", v1_answer)

    show.step("Version 2 (new instructions, same agent name)")
    # TODO 3: Create version 2 that always signs off with '- Contoso HR' and answers in bullet points
    raise NotImplementedError("TODO 3: Create version 2 that always signs off with '- Contoso HR' and answers in bullet points  (see README step and solution/ if stuck)")
    v2_answer = ask(v2, "Who handles payroll disputes?").output_text
    pinned_v1 = ask(v1, "Who handles payroll disputes?").output_text
    show.text("v2", v2_answer)
    show.text("v1 (pinned)", pinned_v1)

    # TODO 4: List all versions of the agent
    raise NotImplementedError("TODO 4: List all versions of the agent  (see README step and solution/ if stuck)")
    show.kv({"versions": versions})
    openai().conversations.delete(conv.id)
    return {"v1_answer": v1_answer, "v2_answer": v2_answer, "pinned_v1": pinned_v1, "versions": versions}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
