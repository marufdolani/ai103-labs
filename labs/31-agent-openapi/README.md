# Lab 31 · Agent with an OpenAPI tool

**Scenario.** Contoso's travel agent should check live weather before giving packing advice. A REST API with an OpenAPI 3 spec already exists, and the team doesn't want to host any glue code. You'll give the agent an **OpenAPI tool**: the Agent Service calls the API itself.

**Exam objectives.** D2 › *Integrate agent tools, including APIs*; *integrate generative workflows … by using Foundry SDKs and connectors*.

**You will learn**
- `OpenApiTool(openapi=OpenApiFunctionDefinition(name, spec, auth))`. Every `operationId` becomes a callable function.
- Auth options: **anonymous**, **project connection** (API key stored in a connection), **managed identity** (`OpenApiManagedAuthDetails` with an audience). No secrets in code.
- The difference from function calling: no client-side execution loop.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Wrap `weather_openapi.json` in an `OpenApiTool` (anonymous auth). | Good `operationId`s and descriptions drive tool selection. |
| 2 | Agent with the tool. | |
| 3 | Ask, then find the OpenAPI call items. | Verify the agent used live data. |

## Run and test
```bash
./lab run 31 && ./lab validate 31      # one click: ./lab solve 31
```

## Explore
- For an internal API protected by Entra ID, use `OpenApiManagedAuthDetails(security_scheme=OpenApiManagedSecurityScheme(audience="api://<app-id>"))` and grant the **project's managed identity** access.
- Azure Functions as tools: `AzureFunctionTool` (queue-based) for long-running work.

## Exam reflexes
- "Agent calls our REST API described by OpenAPI, no app code" → **OpenAPI tool** (+ managed identity auth for internal APIs).
- "Logic must run in our app process" → **function calling**. "Tools hosted behind a standard protocol" → **MCP** (lab 32).

## Clean up
`./lab clean 31`
