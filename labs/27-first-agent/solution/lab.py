"""Lab 27 - First prompt agent with versions."""
from azure.ai.projects.models import PromptAgentDefinition

from labkit import cfg, show
from labkit.agents import ask, delete_agent
from labkit.clients import openai, project

AGENT = "lab27-hr-helpdesk"


def main() -> dict:
    delete_agent(AGENT)

    show.step("Version 1")
    # >>> TODO 1: Create version 1: role, goal and boundaries in the instructions
    v1 = project().agents.create_version(
        agent_name=AGENT,
        description="Answers general HR questions for Contoso employees",
        definition=PromptAgentDefinition(
            model=cfg("CHAT_MODEL"),
            instructions=("Role: Contoso HR helpdesk agent. Goal: help employees with HR questions in under 80 words. "
                          "Boundaries: never give legal or medical advice; for payroll disputes, refer to hr@contoso.example."),
        ),
        metadata={"owner": "hr-platform", "lab": "27"},
    )
    # <<<
    show.kv({"name": v1.name, "version": v1.version, "id": v1.id})

    show.step("Conversation with v1")
    # >>> TODO 2: Create a conversation and ask two related questions with the agent reference
    conv = openai().conversations.create()
    ask(v1, "Hi, I'm Alex from the Lisbon office.", conversation=conv.id)
    v1_answer = ask(v1, "Who should I contact about a payroll dispute, and what's my name?", conversation=conv.id).output_text
    # <<<
    show.text("v1", v1_answer)

    show.step("Version 2 (new instructions, same agent name)")
    # >>> TODO 3: Create version 2 that always signs off with '- Contoso HR' and answers in bullet points
    v2 = project().agents.create_version(
        agent_name=AGENT,
        definition=PromptAgentDefinition(
            model=cfg("CHAT_MODEL"),
            instructions=("Role: Contoso HR helpdesk agent. Answer in short bullet points and always end with the line "
                          "'- Contoso HR'. Never give legal or medical advice; payroll disputes go to hr@contoso.example."),
        ),
    )
    # <<<
    v2_answer = ask(v2, "Who handles payroll disputes?").output_text
    pinned_v1 = ask(v1, "Who handles payroll disputes?").output_text
    show.text("v2", v2_answer)
    show.text("v1 (pinned)", pinned_v1)

    # >>> TODO 4: List all versions of the agent
    versions = [v.version for v in project().agents.list_versions(AGENT)]
    # <<<
    show.kv({"versions": versions})
    openai().conversations.delete(conv.id)
    return {"v1_answer": v1_answer, "v2_answer": v2_answer, "pinned_v1": pinned_v1, "versions": versions}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
