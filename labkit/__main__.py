"""Lab CLI.  Usage:  ./lab <command> [lab] [--solution]

  list                     list all labs
  open NN                  show where the lab lives and what it covers
  doctor                   check settings, identity and the deployed platform
  run NN [--solution]      run your starter (default) or the reference solution
  validate NN [--solution] run the lab's validation tests against your code (or the reference)
  solve NN                 one-click: run + validate the reference solution
  validate-all [--solution]
  clean NN                 remove resources the lab created (agents, indexes, files)
  make-starters [--force]  regenerate starter/ files from solution/
  env-from-rg RG           write .env from a Deploy-to-Azure deployment in resource group RG
  env-merge RG DEPLOYMENT  append a lab's extra-infra deployment outputs to .env (labs 06, 08, 11)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

from . import catalog, show
from .config import LABS_DIR, ROOT


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(__doc__)
        return 0
    cmd, args = argv[0], argv[1:]
    impl = "solution" if "--solution" in args else "starter"
    args = [a for a in args if not a.startswith("--")]

    if cmd == "list":
        for domain, label in catalog.DOMAINS.items():
            print(f"\n{domain}  {label}")
            for lab in (l for l in catalog.LABS if l.domain == domain):
                req = f"  [needs: {', '.join(lab.requires)}]" if lab.requires else ""
                print(f"  {lab.id}  {lab.title}  (~{lab.minutes} min){req}")
        return 0

    if cmd == "doctor":
        from .doctor import run

        return run()

    if cmd == "make-starters":
        from .starters import make_all

        written = make_all(force="--force" in argv)
        print(f"Wrote {len(written)} starter files")
        return 0

    if cmd == "env-from-rg":
        return _env_from_rg(args[0] if args else "")

    if cmd == "env-merge":
        return _env_merge(*args[:2]) if len(args) >= 2 else (print("Usage: ./lab env-merge <rg> <deployment>") or 2)

    if not args:
        print("Missing lab number, e.g. ./lab run 01")
        return 2
    lab_id = args[0].zfill(2)
    lab = catalog.get(lab_id)

    if cmd == "open":
        folder = LABS_DIR / lab.folder
        print(f"Lab {lab.id}: {lab.title}\nDomain: {catalog.DOMAINS[lab.domain]}\n"
              f"README : {folder / 'README.md'}\nEdit   : {folder / 'starter' / 'lab.py'}\n"
              f"Run    : ./lab run {lab.id}\nTest   : ./lab validate {lab.id}")
        return 0

    if cmd == "run":
        from .runner import run

        show.title(f"Lab {lab.id} · {lab.title} · {impl}")
        result = run(lab_id, impl)
        show.result(result)
        return 0

    if cmd in {"validate", "solve"}:
        if cmd == "solve":
            impl = "solution"
        return _pytest([str(LABS_DIR / lab.folder / "test_lab.py")], impl)

    if cmd == "validate-all":
        return _pytest([str(LABS_DIR)], impl)

    if cmd == "clean":
        from .runner import load

        module = load(lab_id, "solution")
        if hasattr(module, "cleanup"):
            module.cleanup()
            print("Cleaned up.")
        else:
            print("Nothing to clean for this lab.")
        return 0

    print(__doc__)
    return 2


def _pytest(targets: list[str], impl: str) -> int:
    env = {**os.environ, "LAB_IMPL": impl}
    print(f"Validating {impl} implementation ...")
    return subprocess.call([sys.executable, "-m", "pytest", "-q", "-rs", "-s", *targets], cwd=ROOT, env=env)


def _env_from_rg(resource_group: str) -> int:
    if not resource_group:
        print("Usage: ./lab env-from-rg <resource-group>")
        return 2
    query = "[?properties.outputs.PROJECT_ENDPOINT != null] | sort_by(@, &properties.timestamp) | [-1].properties.outputs"
    raw = subprocess.check_output(["az", "deployment", "group", "list", "-g", resource_group, "--query", query, "-o", "json"], text=True)
    outputs = json.loads(raw or "null")
    if not outputs:
        print(f"No AI-103 platform deployment found in {resource_group}.")
        return 1
    lines = [f'{k}="{v["value"]}"' for k, v in outputs.items()]
    (ROOT / ".env").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} settings to .env")
    return 0


def _env_merge(resource_group: str, deployment: str) -> int:
    raw = subprocess.check_output(["az", "deployment", "group", "show", "-g", resource_group, "-n", deployment,
                                   "--query", "properties.outputs", "-o", "json"], text=True)
    outputs = json.loads(raw or "null") or {}
    env_file = ROOT / ".env"
    existing = env_file.read_text(encoding="utf-8").splitlines() if env_file.exists() else []
    keep = [l for l in existing if l.split("=", 1)[0] not in outputs]
    keep += [f'{k}="{v["value"]}"' for k, v in outputs.items()]
    env_file.write_text("\n".join(keep) + "\n", encoding="utf-8")
    print(f"Merged {len(outputs)} settings into .env: {', '.join(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
