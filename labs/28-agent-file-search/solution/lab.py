"""Lab 28 - Agent with File Search (managed vector store, citations)."""
from azure.ai.projects.models import FileSearchTool, PromptAgentDefinition

from labkit import cfg, show
from labkit.agents import ask, citations, delete_agent
from labkit.clients import openai, project
from labkit.rag import POLICY_DIR

AGENT = "lab28-policy-agent"
STATE: dict = {}


def build_vector_store() -> str:
    # >>> TODO 1: Create a vector store and upload every policy markdown file into it (upload_and_poll)
    vs = openai().vector_stores.create(name="lab28-policies")
    for path in sorted(POLICY_DIR.glob("*.md")):
        with path.open("rb") as f:
            openai().vector_stores.files.upload_and_poll(vector_store_id=vs.id, file=f)
    return vs.id
    # <<<


def main() -> dict:
    delete_agent(AGENT)
    vs_id = build_vector_store()
    STATE["vector_store"] = vs_id
    show.ok(f"vector store {vs_id} ready")

    # >>> TODO 2: Create the agent with a FileSearchTool bound to the vector store
    agent = project().agents.create_version(
        agent_name=AGENT,
        definition=PromptAgentDefinition(
            model=cfg("CHAT_MODEL"),
            instructions="Answer Contoso policy questions using file search only. Cite the policy file. If not found, say so.",
            tools=[FileSearchTool(vector_store_ids=[vs_id], max_num_results=4)],
        ),
    )
    # <<<

    # >>> TODO 3: Ask a question and collect the answer, the file_search_call items and the file citations
    resp = ask(agent, "What's the nightly hotel cap in Sydney, and do I need receipts for a USD 30 taxi?")
    searched = any(item.type == "file_search_call" for item in resp.output)
    cites = [c for c in citations(resp) if c["type"] == "file_citation"]
    # <<<
    show.text("Answer", resp.output_text)
    show.kv({"file search used": searched, "cited files": sorted({c["filename"] for c in cites})})
    return {"answer": resp.output_text, "searched": searched, "cited": sorted({c["filename"] or "" for c in cites})}


def cleanup() -> None:
    delete_agent(AGENT)
    for vs in openai().vector_stores.list():
        if vs.name == "lab28-policies":
            for f in openai().vector_stores.files.list(vector_store_id=vs.id):
                openai().files.delete(f.id)
            openai().vector_stores.delete(vs.id)


if __name__ == "__main__":
    show.result(main())
