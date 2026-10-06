# Lab 29 · Agent with Code Interpreter

**Scenario.** Contoso's sales ops lead uploads a quarterly CSV and asks for totals by region plus a chart for the board deck. LLMs are bad at arithmetic over many rows, so the agent must **run code** in a sandbox.

**Exam objectives.** D2 › *Integrate agent tools, including … custom functions*; *build agents that integrate retrieval, function-calling*; *design tool-augmented flows*.

**You will learn**
- `CodeInterpreterTool(container=AutoCodeInterpreterToolParam(file_ids=[...]))`: a sandboxed Python container with your files.
- `code_interpreter_call` output items; `container_file_citation` annotations for generated files.
- Downloading generated files with `containers.files.content.retrieve`.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Upload the CSV and create the agent with Code Interpreter. | Files go into the agent's container. |
| 2 | Ask for totals and a chart; find generated files in annotations. | Generated artefacts are referenced, not inlined. |
| 3 | Download the PNG. | Bring results back to your app. |

## Run and test
```bash
./lab run 29 && ./lab validate 29      # one click: ./lab solve 29
```
The chart lands in `.out/lab29/`.

## Exam reflexes
- "Compute statistics, transform data, plot charts from uploaded files" → **Code Interpreter**.
- Arithmetic over data → code, never the model's head (same lesson as lab 22).

## Clean up
`./lab clean 29`
