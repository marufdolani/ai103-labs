"""Platform health check: settings, identity, model deployments, search, storage."""
from __future__ import annotations

from . import show
from .config import cfg, enabled

REQUIRED = [
    "PROJECT_ENDPOINT", "FOUNDRY_ENDPOINT", "FOUNDRY_OPENAI_ENDPOINT", "CHAT_MODEL", "SMALL_MODEL",
    "LARGE_MODEL", "EMBEDDING_MODEL", "SEARCH_ENDPOINT", "STORAGE_BLOB_ENDPOINT",
]
OPTIONAL = ["ROUTER_MODEL", "IMAGE_MODEL", "VIDEO_MODEL", "AUDIO_MODELS_ENABLED", "LEGACY_CHAT_MODEL",
            "APIM_GATEWAY_URL", "GUARDED_MODEL"]


def run() -> int:
    failures = 0
    show.title("Settings")
    for name in REQUIRED:
        value = cfg(name, required=False)
        print(f"   {'ok ' if value else 'MISSING'} {name} = {value or '-'}")
        failures += 0 if value else 1
    for name in OPTIONAL:
        print(f"   {'on ' if enabled(name) else 'off'} {name}")
    if failures:
        show.warn("Fix missing settings first (run `azd up`, or `./lab env-from-rg <rg>`).")
        return 1

    checks = [
        ("Entra ID token", _token),
        ("Project deployments", _deployments),
        (f"Model call ({cfg('SMALL_MODEL')})", _model_call),
        ("Embeddings", _embeddings),
        ("Azure AI Search", _search),
        ("Blob Storage", _storage),
    ]
    show.title("Live checks")
    for label, fn in checks:
        try:
            detail = fn()
            show.ok(f"{label}: {detail}")
        except Exception as exc:  # noqa: BLE001 - we want every failure reported
            failures += 1
            show.warn(f"{label}: {type(exc).__name__}: {str(exc)[:300]}")
    if failures:
        show.warn("Some checks failed. New role assignments can take ~5 minutes to apply; try again.")
    return 1 if failures else 0


def _token() -> str:
    from .clients import token

    return f"acquired ({len(token())} chars)"


def _deployments() -> str:
    from .clients import project

    names = sorted(d.name for d in project().deployments.list())
    return ", ".join(names)


def _model_call() -> str:
    from .clients import openai

    resp = openai().responses.create(model=cfg("SMALL_MODEL"), input="Reply with the single word: ready",
                                     reasoning={"effort": "low"}, max_output_tokens=200)
    return resp.output_text.strip()[:40]


def _embeddings() -> str:
    from .clients import embed

    return f"{len(embed(['hello'])[0])} dimensions"


def _search() -> str:
    from .clients import search_index_client

    return f"{len(list(search_index_client().list_index_names()))} indexes"


def _storage() -> str:
    from .clients import blob_service

    return ", ".join(c.name for c in blob_service().list_containers())
