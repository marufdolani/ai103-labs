"""Lab 33 - Agent grounded on Azure AI Search, with security trimming."""
from azure.ai.projects.models import (AISearchIndexResource, AzureAISearchTool, AzureAISearchToolResource,
                                      PromptAgentDefinition)

from labkit import cfg, show
from labkit.agents import ask, citations, delete_agent
from labkit.clients import project
from labkit.rag import INDEX_NAME, ensure_policy_index

INSTRUCTIONS = ("Answer Contoso policy questions ONLY from the search tool results and cite them. "
                "If the results don't contain the answer, say you can't find it.")


def make_agent(name: str, group_filter: str | None):
    # >>> TODO 1: Resolve the 'search' project connection ID and build an AzureAISearchTool (hybrid + semantic, top 4, optional filter)
    connection_id = project().connections.get(cfg("SEARCH_CONNECTION_NAME", "search")).id
    index = AISearchIndexResource(project_connection_id=connection_id, index_name=INDEX_NAME,
                                  query_type="vector_semantic_hybrid", top_k=4, filter=group_filter)
    tool = AzureAISearchTool(azure_ai_search=AzureAISearchToolResource(indexes=[index]))
    # <<<
    delete_agent(name)
    return project().agents.create_version(agent_name=name, definition=PromptAgentDefinition(
        model=cfg("CHAT_MODEL"), instructions=INSTRUCTIONS, tools=[tool]))


def main() -> dict:
    ensure_policy_index()
    hr_agent = make_agent("lab33-hr-agent", None)
    # >>> TODO 2: A second agent for all staff that can only see documents tagged 'all-staff' (security trimming via filter)
    staff_agent = make_agent("lab33-staff-agent", "group_ids/any(g: g eq 'all-staff')")
    # <<<

    q_leave = "How many weeks of parental leave does a primary caregiver get?"
    q_bonus = "What percentage of base salary is the annual bonus pool?"
    r1 = ask(staff_agent, q_leave)
    r2 = ask(staff_agent, q_bonus)
    r3 = ask(hr_agent, q_bonus)
    # >>> TODO 3: Collect citations from the grounded answer
    cites = citations(r1)
    # <<<
    show.text("Staff agent: leave", r1.output_text)
    show.text("Staff agent: bonus (restricted doc)", r2.output_text)
    show.text("HR agent: bonus", r3.output_text)
    show.kv({"citations": cites[:3]})
    return {"leave": r1.output_text, "bonus_staff": r2.output_text, "bonus_hr": r3.output_text, "citations": cites}


def cleanup() -> None:
    for name in ("lab33-hr-agent", "lab33-staff-agent"):
        delete_agent(name)


if __name__ == "__main__":
    show.result(main())
