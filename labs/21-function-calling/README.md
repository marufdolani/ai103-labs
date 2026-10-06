# Lab 21 · Function calling loop

**Scenario.** Contoso's order assistant must answer from the live order system, never from the model's imagination. You'll expose two functions, let the model decide when to call them (possibly in parallel), execute them in your code, and loop until the model can answer.

**Exam objectives.** D2 › *Design workflows, tool-augmented flows, and multistep reasoning pipelines*; *define … tool schemas*.

**You will learn**
- Tool schemas with JSON Schema, `strict: true`, enums.
- The loop: model returns `function_call` items → **your code runs them** → send `function_call_output` (matched by `call_id`) → repeat.
- Bounding the loop (`max_rounds`) as a safeguard.

## Steps
| TODO | Build | Why |
|---|---|---|
| - | Read the `TOOLS` schemas first. | Strict mode = every property required + `additionalProperties: false`. |
| 1 | First request with `tools=`. | The model decides whether a tool is needed. |
| 2 | Execute all calls, return outputs with `previous_response_id`. | Parallel calls arrive in one turn; answer them all. |

## Run and test
```bash
./lab run 21 && ./lab validate 21      # one click: ./lab solve 21
```

## Explore
- Set `parallel_tool_calls=False` and count rounds.
- Add `tool_choice={"type": "function", "name": "get_order_status"}` to force a call.
- Ask about order 1234. The function returns an error, and the model should say it couldn't find it.

## Exam reflexes
- Function calling: **the model chooses, your app executes**. A service-side API call with no app code → **OpenAPI tool** (lab 31).
- Arguments are model-generated JSON. Validate them before acting, especially for consequential actions (lab 37).

## Clean up
Nothing to clean.
