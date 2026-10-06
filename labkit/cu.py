"""Azure Content Understanding (Foundry Tools) REST helpers. GA API 2025-11-01, keyless."""
from __future__ import annotations

from .clients import Rest, RestError
from .config import cfg

API = "2025-11-01"
SAMPLES = "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data"


def set_defaults() -> dict:
    """Map Content Understanding model aliases to this platform's deployments (one-time per resource)."""
    large, emb = cfg("LARGE_MODEL"), cfg("EMBEDDING_MODEL")
    body = {"modelDeployments": {
        large: large,
        "text-embedding-3-large": emb,
        "prebuilt-analyzer-completion": large,
        "prebuilt-analyzer-completion-mini": large,
        "prebuilt-analyzer-embedding": emb,
    }}
    return Rest().patch(f"contentunderstanding/defaults?api-version={API}", body).json()


def create_analyzer(analyzer_id: str, definition: dict) -> dict:
    rest = Rest()
    rest.delete(f"contentunderstanding/analyzers/{analyzer_id}?api-version={API}")
    resp = rest.put(f"contentunderstanding/analyzers/{analyzer_id}?api-version={API}", definition)
    op = resp.headers.get("Operation-Location")
    return rest.poll(op) if op else resp.json()


def analyze_url(analyzer_id: str, url: str, timeout: float = 900) -> dict:
    rest = Rest()
    resp = rest.post(f"contentunderstanding/analyzers/{analyzer_id}:analyze?api-version={API}", {"inputs": [{"url": url}]})
    return rest.poll(resp.headers["Operation-Location"], interval=3, timeout=timeout)["result"]


def analyze_bytes(analyzer_id: str, data: bytes, content_type: str, timeout: float = 600) -> dict:
    rest = Rest()
    resp = rest.request("POST", f"contentunderstanding/analyzers/{analyzer_id}:analyzeBinary?api-version={API}",
                        data=data, headers={"Content-Type": content_type})
    return rest.poll(resp.headers["Operation-Location"], interval=3, timeout=timeout)["result"]


def field_value(field: dict | None):
    """Return the typed value of a Content Understanding field (valueString, valueNumber, ...)."""
    if not field:
        return None
    for key, value in field.items():
        if key.startswith("value"):
            if key == "valueArray":
                return [field_value(v) for v in value]
            if key == "valueObject":
                return {k: field_value(v) for k, v in value.items()}
            return value
    return None


def delete_analyzer(analyzer_id: str) -> None:
    try:
        Rest().delete(f"contentunderstanding/analyzers/{analyzer_id}?api-version={API}")
    except RestError:
        pass
