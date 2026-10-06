"""Lab 31 - Agent with an OpenAPI tool (service-side API calls, no app code)."""
import json
from pathlib import Path

from azure.ai.projects.models import (OpenApiAnonymousAuthDetails, OpenApiFunctionDefinition, OpenApiTool,
                                      PromptAgentDefinition)

from labkit import cfg, show
from labkit.agents import ask, delete_agent
from labkit.clients import project

AGENT = "lab31-travel-weather"
SPEC = json.loads((Path(__file__).parent / "weather_openapi.json").read_text(encoding="utf-8"))


def main() -> dict:
    delete_agent(AGENT)
    # >>> TODO 1: Wrap the spec in an OpenApiTool with anonymous auth
    weather_tool = OpenApiTool(openapi=OpenApiFunctionDefinition(
        name="weather",
        description="Current weather for any city",
        spec=SPEC,
        auth=OpenApiAnonymousAuthDetails(),
    ))
    # <<<
    # >>> TODO 2: Create the agent with the OpenAPI tool
    agent = project().agents.create_version(
        agent_name=AGENT,
        definition=PromptAgentDefinition(
            model=cfg("CHAT_MODEL"),
            instructions="You help Contoso travellers pack. Always check live weather with the weather tool before advising.",
            tools=[weather_tool],
        ),
    )
    # <<<
    # >>> TODO 3: Ask, then find the OpenAPI tool call items in the output
    resp = ask(agent, "I'm flying to Tokyo tomorrow. What's the weather like now, and should I pack an umbrella?")
    tool_items = [item.type for item in resp.output if "openapi" in item.type]
    # <<<
    show.text("Answer", resp.output_text)
    show.kv({"output item types": [i.type for i in resp.output]})
    return {"answer": resp.output_text, "openapi_items": tool_items, "item_types": [i.type for i in resp.output]}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
