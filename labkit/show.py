"""Console output helpers so every lab prints results the same way."""
from __future__ import annotations

import json
from typing import Any, Iterable, Sequence


def title(text: str) -> None:
    print(f"\n=== {text} " + "=" * max(0, 70 - len(text)))


def step(text: str) -> None:
    print(f"\n-> {text}")


def ok(text: str) -> None:
    print(f"   [ok] {text}")


def warn(text: str) -> None:
    print(f"   [!]  {text}")


def kv(data: dict[str, Any]) -> None:
    width = max((len(str(k)) for k in data), default=0)
    for key, value in data.items():
        print(f"   {str(key).ljust(width)} : {value}")


def table(rows: Iterable[Sequence[Any]], headers: Sequence[str]) -> None:
    rows = [[_fmt(c) for c in r] for r in rows]
    widths = [max(len(str(h)), *(len(r[i]) for r in rows)) if rows else len(h) for i, h in enumerate(headers)]
    print("   " + " | ".join(str(h).ljust(w) for h, w in zip(headers, widths)))
    print("   " + "-+-".join("-" * w for w in widths))
    for r in rows:
        print("   " + " | ".join(c.ljust(w) for c, w in zip(r, widths)))


def text(label: str, value: str, limit: int = 600) -> None:
    value = (value or "").strip()
    if len(value) > limit:
        value = value[:limit] + " ..."
    print(f"   {label}:\n      " + value.replace("\n", "\n      "))


def result(data: Any) -> None:
    title("Result returned to the validator")
    print(json.dumps(data, indent=2, default=str)[:4000])


def _fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:,.3f}"
    return str(value)
