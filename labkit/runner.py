"""Load and run a lab implementation (starter or solution)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from . import catalog
from .config import LABS_DIR, cfg, enabled


def lab_dir(lab_id: str) -> Path:
    lab = catalog.get(lab_id)
    path = LABS_DIR / lab.folder
    if not path.exists():
        raise SystemExit(f"Folder missing: {path}")
    return path


def missing_requirements(lab_id: str) -> list[str]:
    """Return human-readable hints for optional capabilities this lab needs but which aren't configured."""
    hints = []
    for req in catalog.get(lab_id).requires:
        env_name, how = catalog.REQUIREMENTS[req]
        if not enabled(env_name):
            hints.append(f"'{req}' not configured ({env_name}). Enable with: {how}")
    return hints


def load(lab_id: str, impl: str = "starter") -> ModuleType:
    folder = lab_dir(lab_id) / impl
    path = folder / "lab.py"
    if not path.exists():
        raise SystemExit(f"{path} not found. Run: ./lab make-starters")
    # Make sibling helper modules importable (e.g. tools.py next to lab.py).
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location(f"lab{lab_id}_{impl}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def run(lab_id: str, impl: str = "starter") -> dict:
    hints = missing_requirements(lab_id)
    if hints:
        raise SystemExit("Lab needs optional setup:\n  " + "\n  ".join(hints))
    cfg("PROJECT_ENDPOINT")  # fail fast with a clear message if .env is missing
    module = load(lab_id, impl)
    return module.main()
