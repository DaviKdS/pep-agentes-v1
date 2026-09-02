#!/usr/bin/env python3
"""Wrapper compativel para instalar o PEP-Agentes no Claude Code."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pep.core.models import Scope  # noqa: E402
from pep.providers.claude import ClaudeProvider  # noqa: E402
from pep.services.manager import format_results, resolve_scopes  # noqa: E402

_PROVIDER = ClaudeProvider()
PACKAGE_ROOT = _PROVIDER.source_claude_md.parents[1]
SOURCE_CLAUDE_MD = _PROVIDER.source_claude_md
SOURCE_COMMAND = _PROVIDER.source_command


def read_block() -> str:
    return _PROVIDER.block()


def targets_for(scope_dir: Path, is_global: bool) -> tuple[Path, Path]:
    return _PROVIDER.targets_for(Scope(scope_dir, is_global))


def install_target(
    scope_dir: Path,
    block: str | None = None,
    command_text: str | None = None,
    is_global: bool = False,
    force: bool = False,
) -> None:
    del block, command_text
    result = _PROVIDER.install(Scope(scope_dir, is_global), force=force)
    for line in result.messages:
        print(f"  {line}")


def uninstall_target(scope_dir: Path, is_global: bool = False) -> None:
    result = _PROVIDER.uninstall(Scope(scope_dir, is_global))
    for line in result.messages:
        print(f"  {line}")


def interactive_scopes() -> list[Scope]:
    print("Onde instalar o PEP-Agentes para o Claude Code?")
    print("  1) So este projeto (diretorio atual)")
    print("  2) Projetos especificos (informe os caminhos)")
    print("  3) Global (~/.claude, vale para todos os projetos)")
    choice = input("Escolha [1/2/3]: ").strip()
    if choice == "1":
        return [Scope(Path.cwd(), False)]
    if choice == "2":
        raw = input("Caminhos separados por virgula: ").strip()
        return [Scope(Path(p.strip()).expanduser().resolve(), False) for p in raw.split(",") if p.strip()]
    if choice == "3":
        return [Scope(Path.home() / ".claude", True)]
    print("Opcao invalida.")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Instala o PEP-Agentes para o Claude Code.")
    parser.add_argument("--here", action="store_true", help="instalar no diretorio atual")
    parser.add_argument("--path", action="append", metavar="CAMINHO", help="instalar em projeto especifico")
    parser.add_argument("--global", dest="global_scope", action="store_true", help="instalar em ~/.claude")
    parser.add_argument("--force", action="store_true", help="sobrescrever pep.md existente")
    parser.add_argument("--uninstall", action="store_true", help="remover o PEP dos alvos")
    args = parser.parse_args()

    scopes = resolve_scopes(args.here, args.path, False)
    if args.global_scope:
        scopes.append(Scope(Path.home() / ".claude", True))
    if not scopes:
        scopes = interactive_scopes()
    if not scopes:
        print("Nenhum alvo selecionado.")
        return 2

    results = [
        _PROVIDER.uninstall(scope) if args.uninstall else _PROVIDER.install(scope, force=args.force)
        for scope in scopes
    ]
    print(format_results(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
