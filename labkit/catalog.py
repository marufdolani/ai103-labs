"""Catalog of the 50 AI-103 labs. Drives the CLI, the README table and requirement checks."""
from __future__ import annotations

from dataclasses import dataclass, field

DOMAINS = {
    "D1": "Plan and manage an Azure AI solution (25-30%)",
    "D2": "Implement generative AI and agentic solutions (30-35%)",
    "D3": "Implement computer vision solutions (10-15%)",
    "D4": "Implement text analysis solutions (10-15%)",
    "D5": "Implement information extraction solutions (10-15%)",
}

# Optional capabilities. A lab that needs one is skipped (not failed) when it isn't available.
REQUIREMENTS = {
    "router": ("ROUTER_MODEL", "azd env set DEPLOY_MODEL_ROUTER true && azd provision"),
    "image": ("IMAGE_MODEL", "azd env set DEPLOY_IMAGE_MODEL true && azd provision"),
    "video": ("VIDEO_MODEL", "azd env set DEPLOY_VIDEO_MODEL true && azd provision"),
    "audio": ("AUDIO_MODELS_ENABLED", "azd env set DEPLOY_AUDIO_MODELS true && azd provision"),
    "legacy": ("LEGACY_CHAT_MODEL", "azd env set DEPLOY_LEGACY_CHAT true && azd provision"),
    "apim": ("APIM_GATEWAY_URL", "deploy labs/06-ai-gateway/infra (see the lab README)"),
    "guarded": ("GUARDED_MODEL", "deploy labs/11-guardrails-blocklist/infra (see the lab README)"),
    "network": ("ISOLATED_FOUNDRY_NAME", "deploy labs/08-private-networking/infra (see the lab README)"),
}


@dataclass(frozen=True)
class Lab:
    id: str
    slug: str
    title: str
    domain: str
    minutes: int
    requires: tuple[str, ...] = field(default_factory=tuple)

    @property
    def folder(self) -> str:
        return f"{self.id}-{self.slug}"


LABS: list[Lab] = [
    # ---- D1: plan, manage, secure, responsible AI ----
    Lab("01", "platform-tour", "Provision and tour the Foundry platform", "D1", 20),
    Lab("02", "keyless-auth", "Keyless access with Entra ID and disabled keys", "D1", 20),
    Lab("03", "model-selection", "Choose the right model: small, large, reasoning", "D1", 25),
    Lab("04", "quotas-429", "Quotas, rate limits and resilient retries", "D1", 20),
    Lab("05", "model-router", "Route prompts with model router", "D1", 15, ("router",)),
    Lab("06", "ai-gateway", "AI gateway: per-app token limits with API Management", "D1", 45, ("apim",)),
    Lab("07", "cicd-eval-gate", "CI/CD for Foundry with an evaluation gate", "D1", 35),
    Lab("08", "private-networking", "Network-isolate the AI platform", "D1", 40, ("network",)),
    Lab("09", "rbac-least-privilege", "Least-privilege RBAC for AI teams", "D1", 25),
    Lab("10", "monitor-cost", "Monitor tokens, latency, drift and cost", "D1", 30),
    Lab("11", "guardrails-blocklist", "Custom guardrail: thresholds, shields, blocklists", "D1", 30, ("guarded",)),
    Lab("12", "prompt-shields", "Prompt Shields: direct and indirect attacks", "D1", 20),
    Lab("13", "groundedness-protected", "Groundedness and protected-material detection", "D1", 20),
    Lab("14", "evaluate-quality-safety", "Quality and safety evaluations", "D1", 30),
    Lab("15", "red-teaming", "Automated red teaming", "D1", 30),
    Lab("16", "audit-trail", "Audit trail: traces, provenance, approvals", "D1", 25),
    # ---- D2: generative apps ----
    Lab("17", "responses-chat", "Chat app with the Responses API", "D2", 20),
    Lab("18", "prompt-parameters", "Prompt engineering and generation parameters", "D2", 25),
    Lab("19", "structured-outputs", "Structured outputs for downstream systems", "D2", 20),
    Lab("20", "rag-from-scratch", "RAG from scratch with hybrid and semantic search", "D2", 40),
    Lab("21", "function-calling", "Function calling loop", "D2", 25),
    Lab("22", "multistep-pipeline", "Multistep reasoning pipeline", "D2", 25),
    Lab("23", "reflection-loop", "Reflection and self-critique loop", "D2", 25),
    Lab("24", "hybrid-rules-orchestration", "Hybrid LLM + rules engine, multi-model orchestration", "D2", 30),
    Lab("25", "fine-tuning-prep", "Fine-tuning: decide, prepare data, submit", "D2", 30),
    Lab("26", "evaluate-rag-variants", "Evaluate and compare app variants", "D2", 30),
    # ---- D2: agents ----
    Lab("27", "first-agent", "First prompt agent with versions", "D2", 20),
    Lab("28", "agent-file-search", "Agent with File Search", "D2", 20),
    Lab("29", "agent-code-interpreter", "Agent with Code Interpreter", "D2", 20),
    Lab("30", "agent-functions-memory", "Agent with custom functions and memory", "D2", 30),
    Lab("31", "agent-openapi", "Agent with an OpenAPI tool", "D2", 20),
    Lab("32", "agent-mcp-approval", "Agent with MCP: approvals and allow-lists", "D2", 25),
    Lab("33", "agent-search-grounding", "Agent grounded on Azure AI Search", "D2", 25),
    Lab("34", "multiagent-sequential-concurrent", "Multi-agent: sequential and concurrent", "D2", 30),
    Lab("35", "multiagent-handoff-groupchat", "Multi-agent: handoff, group chat, Magentic", "D2", 35),
    Lab("36", "a2a-delegation", "Agent-to-agent (A2A) discovery and delegation", "D2", 30),
    Lab("37", "approval-workflow", "Semi-autonomous workflow with safeguards", "D2", 30),
    Lab("38", "agent-observability", "Agent tracing, evaluation and error analysis", "D2", 30),
    # ---- D3: vision ----
    Lab("39", "image-generation", "Generate and edit images", "D3", 25, ("image",)),
    Lab("40", "video-generation", "Generate and remix video", "D3", 30, ("video",)),
    Lab("41", "multimodal-understanding", "Captions, visual Q&A and alt text", "D3", 25),
    Lab("42", "content-understanding-visual", "Content Understanding for images and video", "D3", 35),
    Lab("43", "multimodal-safety", "Responsible AI for images", "D3", 25),
    # ---- D4: text and speech ----
    Lab("44", "language-analysis", "Text analysis: Language service vs LLM", "D4", 30),
    Lab("45", "translation", "Translate text and documents", "D4", 30),
    Lab("46", "speech-basics", "Speech to text, text to speech, SSML, translation", "D4", 30),
    Lab("47", "voice-agent", "Speech as an agent modality", "D4", 30, ("audio",)),
    # ---- D5: information extraction ----
    Lab("48", "search-enrichment", "Ingestion with skillsets and integrated vectorization", "D5", 45),
    Lab("49", "document-extraction", "Document Intelligence vs Content Understanding", "D5", 35),
    Lab("50", "capstone", "Capstone: governed, grounded knowledge agent", "D5", 60),
]

BY_ID = {lab.id: lab for lab in LABS}


def get(lab_id: str) -> Lab:
    key = lab_id.zfill(2)
    if key not in BY_ID:
        raise SystemExit(f"Unknown lab '{lab_id}'. Run: ./lab list")
    return BY_ID[key]
