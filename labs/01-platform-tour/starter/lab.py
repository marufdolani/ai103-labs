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
    # TODO 1: List deployments as dicts with name, model, version, sku and capacity
    raise NotImplementedError("TODO 1: List deployments as dicts with name, model, version, sku and capacity  (see README step and solution/ if stuck)")
    show.table([[d["name"], d["model"], d["version"], d["sku"], d["capacity"]] for d in deployments],
               ["deployment", "model", "version", "sku", "capacity (K TPM)"])

    show.step("Project connections")
    # TODO 2: List connections as dicts with name and type
    raise NotImplementedError("TODO 2: List connections as dicts with name and type  (see README step and solution/ if stuck)")
    show.table([[c["name"], c["type"]] for c in connections], ["connection", "type"])

    show.step("Application Insights (for tracing)")
    # TODO 3: Get the Application Insights connection string from the project telemetry operations
    raise NotImplementedError("TODO 3: Get the Application Insights connection string from the project telemetry operations  (see README step and solution/ if stuck)")
    show.ok("connection string retrieved" if ai_conn else "no App Insights connected")

    show.step("First call through the project")
    # TODO 4: Call the chat deployment with the Responses API and keep the output text
    raise NotImplementedError("TODO 4: Call the chat deployment with the Responses API and keep the output text  (see README step and solution/ if stuck)")
    show.text("Answer", answer)

    return {
        "deployments": [d["name"] for d in deployments],
        "connection_types": sorted({c["type"].split(".")[-1].lower() for c in connections}),
        "appinsights_connected": bool(ai_conn),
        "answer": answer,
    }


if __name__ == "__main__":
    show.result(main())
