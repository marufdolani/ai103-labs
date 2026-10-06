"""Shared configuration for azure-ai-evaluation (AI-assisted judges and safety evaluators)."""
from __future__ import annotations

from .clients import credential
from .config import cfg

# Judge deployments are reasoning models (GPT-5 family), so evaluators need this flag.
REASONING_JUDGE = {"is_reasoning_model": True}


def judge_config() -> dict:
    """Model configuration for AI-assisted evaluators (keyless)."""
    return {
        "azure_endpoint": cfg("FOUNDRY_OPENAI_ENDPOINT"),
        "azure_deployment": cfg("LARGE_MODEL"),
        "api_version": "2025-04-01-preview",
        "credential": credential(),
    }


def project_endpoint() -> str:
    """Safety evaluators and result logging use the Foundry project endpoint."""
    return cfg("PROJECT_ENDPOINT")
