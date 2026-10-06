"""Authenticated clients. Everything is keyless (Microsoft Entra ID via DefaultAzureCredential)."""
from __future__ import annotations

import time
from functools import lru_cache
from typing import Any

import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from .config import cfg

COGNITIVE_SCOPE = "https://cognitiveservices.azure.com/.default"
ARM_SCOPE = "https://management.azure.com/.default"
SEARCH_SCOPE = "https://search.azure.com/.default"


@lru_cache(maxsize=1)
def credential() -> DefaultAzureCredential:
    """Uses `az login` / `azd auth login` locally, managed identity in Azure."""
    return DefaultAzureCredential()


@lru_cache(maxsize=1)
def project():
    """Foundry project client: agents, connections, deployments, evaluations, telemetry."""
    from azure.ai.projects import AIProjectClient

    return AIProjectClient(endpoint=cfg("PROJECT_ENDPOINT"), credential=credential())


@lru_cache(maxsize=1)
def openai():
    """OpenAI client scoped to the Foundry project (responses, conversations, files, vector stores, agents)."""
    return project().get_openai_client()


@lru_cache(maxsize=1)
def aoai():
    """OpenAI v1 client on the Foundry resource (embeddings, images, videos, audio, model deployments)."""
    from openai import OpenAI

    return OpenAI(
        base_url=f"{cfg('FOUNDRY_OPENAI_ENDPOINT').rstrip('/')}/openai/v1/",
        api_key=get_bearer_token_provider(credential(), COGNITIVE_SCOPE),
    )


def token(scope: str = COGNITIVE_SCOPE) -> str:
    return credential().get_token(scope).token


class Rest:
    """Small REST helper for Foundry Tools data-plane APIs (Content Safety, Content Understanding, ...)."""

    def __init__(self, base: str | None = None, scope: str = COGNITIVE_SCOPE):
        self.base = (base or cfg("FOUNDRY_ENDPOINT")).rstrip("/")
        self.scope = scope

    def _headers(self, extra: dict | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token(self.scope)}", "Content-Type": "application/json"}
        headers.update(extra or {})
        return headers

    def request(self, method: str, path: str, *, json: Any = None, data: Any = None,
                headers: dict | None = None, ok: tuple[int, ...] = (200, 201, 202, 204)) -> requests.Response:
        url = path if path.startswith("http") else f"{self.base}/{path.lstrip('/')}"
        resp = requests.request(method, url, json=json, data=data, headers=self._headers(headers), timeout=120)
        if resp.status_code not in ok:
            raise RestError(resp)
        return resp

    def get(self, path: str, **kw) -> requests.Response:
        return self.request("GET", path, **kw)

    def post(self, path: str, body: Any = None, **kw) -> requests.Response:
        return self.request("POST", path, json=body, **kw)

    def put(self, path: str, body: Any = None, **kw) -> requests.Response:
        return self.request("PUT", path, json=body, **kw)

    def patch(self, path: str, body: Any = None, **kw) -> requests.Response:
        return self.request("PATCH", path, json=body, **kw)

    def delete(self, path: str, **kw) -> requests.Response:
        return self.request("DELETE", path, ok=(200, 202, 204, 404), **kw)

    def poll(self, operation_url: str, *, interval: float = 2.0, timeout: float = 600) -> dict:
        """Poll an async operation (Operation-Location) until it finishes."""
        deadline = time.time() + timeout
        while True:
            body = self.get(operation_url).json()
            status = str(body.get("status", "")).lower()
            if status in {"succeeded", "failed", "canceled", "cancelled"}:
                if status != "succeeded":
                    raise RuntimeError(f"Operation {status}: {body.get('error') or body}")
                return body
            if time.time() > deadline:
                raise TimeoutError(f"Timed out polling {operation_url}")
            time.sleep(interval)


class RestError(RuntimeError):
    def __init__(self, resp: requests.Response):
        self.status_code = resp.status_code
        self.body = resp.text[:2000]
        super().__init__(f"HTTP {resp.status_code} {resp.request.method} {resp.url}\n{self.body}")


def arm() -> Rest:
    """Azure Resource Manager (control plane)."""
    return Rest("https://management.azure.com", ARM_SCOPE)


def arm_path(resource_id: str, suffix: str = "", api_version: str = "2025-06-01") -> str:
    sep = "&" if "?" in suffix else "?"
    return f"{resource_id}{suffix}{sep}api-version={api_version}"


def search_index_client():
    from azure.search.documents.indexes import SearchIndexClient

    return SearchIndexClient(cfg("SEARCH_ENDPOINT"), credential())


def search_indexer_client():
    from azure.search.documents.indexes import SearchIndexerClient

    return SearchIndexerClient(cfg("SEARCH_ENDPOINT"), credential())


def search_client(index_name: str):
    from azure.search.documents import SearchClient

    return SearchClient(cfg("SEARCH_ENDPOINT"), index_name, credential())


def blob_service():
    from azure.storage.blob import BlobServiceClient

    return BlobServiceClient(cfg("STORAGE_BLOB_ENDPOINT"), credential=credential())


def embed(texts: list[str], dimensions: int | None = None) -> list[list[float]]:
    """Embed text with the deployed embedding model."""
    kwargs = {"dimensions": dimensions} if dimensions else {}
    resp = aoai().embeddings.create(model=cfg("EMBEDDING_MODEL"), input=texts, **kwargs)
    return [d.embedding for d in resp.data]
