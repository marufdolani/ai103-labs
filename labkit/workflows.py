"""Helpers for Microsoft Agent Framework workflow results."""
from __future__ import annotations

from typing import Any


def _role(message: Any) -> str:
    role = getattr(message, "role", "")
    return str(getattr(role, "value", role))


def flatten(outputs: list[Any]) -> list[dict]:
    """Turn workflow outputs (messages, lists of messages, responses) into [{author, role, text}]."""
    rows: list[dict] = []
    for out in outputs:
        items = out if isinstance(out, list) else getattr(out, "messages", None) or [out]
        for m in items:
            text = getattr(m, "text", None)
            if text is None:
                text = str(m)
            rows.append({"author": getattr(m, "author_name", None) or "", "role": _role(m), "text": text})
    return rows


def assistant_turns(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["role"] == "assistant" and r["text"].strip()]
