"""Provider registry for PEP-Agentes Manager."""

from __future__ import annotations

from pep.providers.claude import ClaudeProvider
from pep.providers.codex import CodexProvider


PROVIDERS = {
    "claude": ClaudeProvider(),
    "codex": CodexProvider(),
}


def get_provider(name: str):
    if name not in PROVIDERS:
        raise ValueError(f"Provider desconhecido: {name}")
    return PROVIDERS[name]


def selected_providers(name: str):
    if name == "all":
        return list(PROVIDERS.values())
    return [get_provider(name)]
