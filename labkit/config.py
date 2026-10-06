"""Configuration: reads the .env written by `azd up` (or `./lab env-from-rg`)."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
LABS_DIR = ROOT / "labs"
OUT_DIR = ROOT / ".out"

load_dotenv(ROOT / ".env", override=False)


class MissingSetting(RuntimeError):
    pass


def cfg(name: str, default: str | None = None, *, required: bool = True) -> str:
    """Return a setting from the environment / .env, with a helpful error if missing."""
    value = os.environ.get(name, "").strip().strip('"')
    if value:
        return value
    if default is not None:
        return default
    if required:
        raise MissingSetting(
            f"{name} is not set. Run `azd up` (writes .env) or `./lab env-from-rg <resource-group>` "
            f"after a Deploy-to-Azure deployment."
        )
    return ""


def enabled(name: str) -> bool:
    """True when an optional capability (model name, endpoint or 'True') is configured."""
    value = os.environ.get(name, "").strip().strip('"').lower()
    return bool(value) and value not in {"false", "0", "none"}


def out_path(*parts: str) -> Path:
    """Location for files a lab produces (images, reports). Ignored by git."""
    path = OUT_DIR.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
