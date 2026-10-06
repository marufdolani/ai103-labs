"""Lab 01 - Provision and tour the Foundry platform."""
from labkit import cfg, show
from labkit.clients import openai, project


def main() -> dict:
    show.title("Endpoints")
    show.kv({
        "Project endpoint": cfg("PROJECT_ENDPOINT"),
        "Foundry Tools endpoint": cfg("FOUNDRY_ENDPOINT"),
        "OpenAI endpoint": cfg("FOUNDRY_OPENAI_ENDPOINT"),
    })

    show.step("Model deployments")
    # >>> TODO 1: List deployments as dicts with name, model, version, sku and capacity
    deployments = [
        {
            "name": d.name,
            "model": getattr(d, "model_name", ""),
            "version": getattr(d, "model_version", ""),
            "sku": getattr(getattr(d, "sku", None), "name", ""),
            "capacity": getattr(getattr(d, "sku", None), "capacity", ""),
        }
        for d in project().deployments.list()
    ]
    # <<<
    show.table([[d["name"], d["model"], d["version"], d["sku"], d["capacity"]] for d in deployments],
               ["deployment", "model", "version", "sku", "capacity (K TPM)"])

    show.step("Project connections")
    # >>> TODO 2: List connections as dicts with name and type
    connections = [{"name": c.name, "type": str(c.type)} for c in project().connections.list()]
    # <<<
    show.table([[c["name"], c["type"]] for c in connections], ["connection", "type"])

    show.step("Application Insights (for tracing)")
    # >>> TODO 3: Get the Application Insights connection string from the project telemetry operations
    ai_conn = project().telemetry.get_application_insights_connection_string()
    # <<<
    show.ok("connection string retrieved" if ai_conn else "no App Insights connected")

    show.step("First call through the project")
    # >>> TODO 4: Call the chat deployment with the Responses API and keep the output text
    resp = openai().responses.create(
        model=cfg("CHAT_MODEL"),
        input="In one sentence, what is a Microsoft Foundry project?",
        reasoning={"effort": "low"},
        max_output_tokens=800,
    )
    answer = resp.output_text
    # <<<
    show.text("Answer", answer)

    return {
        "deployments": [d["name"] for d in deployments],
        "connection_types": sorted({c["type"].split(".")[-1].lower() for c in connections}),
        "appinsights_connected": bool(ai_conn),
        "answer": answer,
    }


if __name__ == "__main__":
    show.result(main())
