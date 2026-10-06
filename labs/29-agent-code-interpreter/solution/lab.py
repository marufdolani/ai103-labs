"""Lab 29 - Agent with Code Interpreter: analyse a CSV and produce a chart."""
import csv
import random

from azure.ai.projects.models import AutoCodeInterpreterToolParam, CodeInterpreterTool, PromptAgentDefinition

from labkit import cfg, out_path, show
from labkit.agents import ask, citations, delete_agent
from labkit.clients import openai, project

AGENT = "lab29-analyst"


def make_csv() -> tuple[str, dict]:
    random.seed(103)
    path = out_path("lab29", "sales.csv")
    totals: dict[str, float] = {}
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["month", "region", "revenue_usd"])
        for month in ["2026-07", "2026-08", "2026-09"]:
            for region in ["APAC", "EMEA", "AMER"]:
                value = round(random.uniform(50_000, 150_000), 2)
                totals[region] = round(totals.get(region, 0) + value, 2)
                w.writerow([month, region, value])
    return str(path), totals


def main() -> dict:
    delete_agent(AGENT)
    path, totals = make_csv()

    # >>> TODO 1: Upload the CSV (purpose 'assistants') and create an agent whose Code Interpreter container includes it
    with open(path, "rb") as f:
        uploaded = openai().files.create(file=f, purpose="assistants")
    agent = project().agents.create_version(
        agent_name=AGENT,
        definition=PromptAgentDefinition(
            model=cfg("CHAT_MODEL"),
            instructions="You are a data analyst. Always compute with Python; never estimate.",
            tools=[CodeInterpreterTool(container=AutoCodeInterpreterToolParam(file_ids=[uploaded.id]))],
        ),
    )
    # <<<

    # >>> TODO 2: Ask for totals per region and a bar chart PNG; find the generated file via container_file_citation
    resp = ask(agent, "Using sales.csv, give the total revenue per region for the quarter (2 decimals) and save a "
                      "bar chart as region_totals.png.")
    files = [c for c in citations(resp) if c["type"] == "container_file_citation"]
    # <<<
    ran_code = any(item.type == "code_interpreter_call" for item in resp.output)

    chart_path = None
    # >>> TODO 3: Download the chart from the container
    for c in files:
        if (c["filename"] or "").endswith(".png"):
            content = openai().containers.files.content.retrieve(c["file_id"], container_id=c["container_id"])
            chart_path = out_path("lab29", c["filename"])
            chart_path.write_bytes(content.read())
    # <<<
    show.text("Answer", resp.output_text)
    show.kv({"expected totals": totals, "code ran": ran_code, "chart saved to": chart_path})
    openai().files.delete(uploaded.id)
    return {"answer": resp.output_text, "expected": totals, "ran_code": ran_code,
            "chart": str(chart_path) if chart_path else None}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
