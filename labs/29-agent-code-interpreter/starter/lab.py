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

    # TODO 1: Upload the CSV (purpose 'assistants') and create an agent whose Code Interpreter container includes it
    raise NotImplementedError("TODO 1: Upload the CSV (purpose 'assistants') and create an agent whose Code Interpreter container includes it  (see README step and solution/ if stuck)")

    # TODO 2: Ask for totals per region and a bar chart PNG; find the generated file via container_file_citation
    raise NotImplementedError("TODO 2: Ask for totals per region and a bar chart PNG; find the generated file via container_file_citation  (see README step and solution/ if stuck)")
    ran_code = any(item.type == "code_interpreter_call" for item in resp.output)

    chart_path = None
    # TODO 3: Download the chart from the container
    raise NotImplementedError("TODO 3: Download the chart from the container  (see README step and solution/ if stuck)")
    show.text("Answer", resp.output_text)
    show.kv({"expected totals": totals, "code ran": ran_code, "chart saved to": chart_path})
    openai().files.delete(uploaded.id)
    return {"answer": resp.output_text, "expected": totals, "ran_code": ran_code,
            "chart": str(chart_path) if chart_path else None}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
