# CLAUDE.md: AI-103 hands-on labs

Context for AI assistants working in this repo.

## Purpose
50 scenario-based labs for Microsoft exam AI-103 (Developing AI Apps and Agents on Azure). Learners deploy one shared platform, complete `starter/lab.py`, and validate against live Azure.

## Layout
- `infra/core.bicep`: shared platform (resource-group scope). `infra/main.bicep` wraps it for azd. `infra/azuredeploy.json` is the compiled ARM template for the Deploy to Azure button. **Rebuild it after any Bicep change:** `bicep build infra/core.bicep --outfile infra/azuredeploy.json`. The same applies to `labs/*/infra/*.bicep`.
- `labkit/`: shared code. `catalog.py` is the source of truth for lab IDs, titles, domains and optional requirements. `clients.py` holds all keyless clients.
- `labs/NN-slug/`: `README.md`, `solution/lab.py` (reference), `starter/lab.py` (generated), `test_lab.py` (pytest, receives `result` = `main()` output).

## Conventions
- Keyless everywhere (`DefaultAzureCredential`); never add API keys or connection strings with secrets.
- Learner code goes between `# >>> TODO n: ...` and `# <<<` in solutions. Run `./lab make-starters --force` to regenerate starters. Never hand-edit starters.
- Every lab `main()` returns a dict; tests assert on behaviour (grounding, schema, blocked attacks), not exact wording.
- Chat models are reasoning models (GPT-5 family): use `reasoning={"effort": "low"}` and generous `max_output_tokens`; don't set temperature.
- Labs needing optional capabilities declare them in `catalog.py` (`requires`), so they skip instead of failing.
- README sections: Scenario · Exam objectives · You will learn · Steps (TODO table) · Run and test · Explore · Exam reflexes · Clean up.

## Checks before committing
```bash
python -m labkit make-starters --force
python -m py_compile $(git ls-files '*.py')
python -m pytest --collect-only -q
```
