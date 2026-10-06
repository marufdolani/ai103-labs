"""Generate learner starter files from the reference solutions.

In a solution file, wrap the code the learner must write like this (inside a function):

    # >>> TODO 3: Create the agent version with PromptAgentDefinition
    agent = ...
    # <<<

The starter keeps the comment and replaces the block with `raise NotImplementedError(...)`,
so `./lab validate NN` fails with a precise message until the learner implements it.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from .config import LABS_DIR

START = re.compile(r"^(?P<indent>\s*)# >>> (?P<label>TODO\s*\d+.*)$")
END = re.compile(r"^\s*# <<<\s*$")


def to_starter(source: str) -> str:
    out: list[str] = []
    inside = False
    for line in source.splitlines():
        if not inside:
            m = START.match(line)
            if m:
                inside = True
                indent, label = m.group("indent"), m.group("label").strip()
                out.append(f"{indent}# {label}")
                safe = label.replace('"', "'")
                out.append(f'{indent}raise NotImplementedError("{safe}  (see README step and solution/ if stuck)")')
            else:
                out.append(line)
        elif END.match(line):
            inside = False
    if inside:
        raise ValueError("Unclosed '# >>> TODO' block")
    return "\n".join(out) + "\n"


def make_all(force: bool = False) -> list[Path]:
    written: list[Path] = []
    for solution_dir in sorted(LABS_DIR.glob("*/solution")):
        starter_dir = solution_dir.parent / "starter"
        starter_dir.mkdir(exist_ok=True)
        for src in solution_dir.rglob("*"):
            if src.is_dir() or "__pycache__" in src.parts:
                continue
            dst = starter_dir / src.relative_to(solution_dir)
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists() and not force and dst.stat().st_mtime > src.stat().st_mtime:
                continue  # never overwrite the learner's newer work
            if src.suffix == ".py":
                dst.write_text(to_starter(src.read_text(encoding="utf-8")), encoding="utf-8")
            else:
                shutil.copy2(src, dst)
            written.append(dst)
    return written
