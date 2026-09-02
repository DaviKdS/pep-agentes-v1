"""High-level operations shared by CLI and GUI."""

from __future__ import annotations

from pathlib import Path

from pep.core.detection import doctor_tools
from pep.core.models import OperationResult, Scope, Status
from pep.providers import selected_providers


def resolve_scopes(here: bool = False, paths: list[str] | None = None, global_scope: bool = False) -> list[Scope]:
    scopes: list[Scope] = []
    if here:
        scopes.append(Scope(Path.cwd(), False))
    for raw in paths or []:
        scopes.append(Scope(Path(raw).expanduser().resolve(), False))
    if global_scope:
        from pep.core.paths import user_home

        scopes.append(Scope(user_home() / ".codex", True))
    return scopes


def resolve_provider_scope(provider_name: str, scope: Scope) -> Scope:
    if not scope.is_global:
        return scope
    from pep.core.paths import user_home

    if provider_name == "claude":
        return Scope(user_home() / ".claude", True)
    if provider_name == "codex":
        return Scope(user_home() / ".codex", True)
    return scope


def run_operation(
    action: str,
    provider_name: str,
    scopes: list[Scope],
    force: bool = False,
    legacy_prompt: bool = False,
) -> list[OperationResult]:
    results: list[OperationResult] = []
    for provider in selected_providers(provider_name):
        for scope in scopes:
            provider_scope = resolve_provider_scope(provider.name, scope)
            if action in {"install", "update"}:
                results.append(provider.install(provider_scope, force=force or action == "update", legacy_prompt=legacy_prompt))
            elif action == "uninstall":
                results.append(provider.uninstall(provider_scope, legacy_prompt=legacy_prompt))
            elif action == "repair":
                results.append(provider.repair(provider_scope, legacy_prompt=legacy_prompt))
            else:
                raise ValueError(f"Acao desconhecida: {action}")
    return results


def collect_status(provider_name: str, scopes: list[Scope], legacy_prompt: bool = False) -> list[Status]:
    rows: list[Status] = []
    for provider in selected_providers(provider_name):
        for scope in scopes:
            rows.append(provider.status(resolve_provider_scope(provider.name, scope), legacy_prompt=legacy_prompt))
    return rows


def collect_doctor(provider_name: str = "all", scopes: list[Scope] | None = None, legacy_prompt: bool = False) -> str:
    lines = ["PEP Doctor", ""]
    for tool in doctor_tools():
        status = "OK" if tool.found else "ERRO"
        lines.append(f"{tool.name:.<22} {status} - {tool.detail}")
    if scopes:
        lines.append("")
        for row in collect_status(provider_name, scopes, legacy_prompt=legacy_prompt):
            lines.append(f"{row.provider} {row.scope.label}: {row.state.value} - {row.detail}")
    return "\n".join(lines)


def format_results(results: list[OperationResult]) -> str:
    chunks: list[str] = []
    for result in results:
        chunks.append(f"== {result.provider} | {result.scope.label} ==")
        chunks.extend(result.messages)
        chunks.append("")
    chunks.append("Concluido.")
    return "\n".join(chunks)


def format_status(rows: list[Status]) -> str:
    lines = []
    for row in rows:
        lines.append(f"{row.provider} | {row.scope.label}: {row.state.value} - {row.detail}")
    return "\n".join(lines) if lines else "Nenhum alvo selecionado."
