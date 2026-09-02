#!/usr/bin/env python3
"""Wrapper compativel para instalar PEP-Codex no Codex."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pep.core.models import Scope  # noqa: E402
from pep.providers.codex import CodexProvider  # noqa: E402
from pep.services.manager import format_results, resolve_scopes  # noqa: E402

_PROVIDER = CodexProvider()
ROOT = _PROVIDER.source_agents.parents[1]
SOURCE_AGENTS = _PROVIDER.source_agents
SOURCE_SKILL = _PROVIDER.source_skill
SOURCE_PROMPT = _PROVIDER.source_prompt


def read_block() -> str:
    return _PROVIDER.block()


def project_targets(project: Path) -> tuple[Path, Path]:
    return _PROVIDER.targets_for(Scope(project, False))


def global_targets() -> tuple[Path, Path]:
    return _PROVIDER.targets_for(Scope(Path.home() / ".codex", True))


def install_legacy_prompt(force: bool) -> str:
    dest = _PROVIDER.legacy_prompt_target()
    if dest.exists() and not force:
        return f"ja existe (use --force para atualizar) -> {dest}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_PROMPT, dest)
    return f"instalado -> {dest}"


def remove_legacy_prompt() -> str:
    dest = _PROVIDER.legacy_prompt_target()
    if not dest.exists():
        return f"inexistente -> {dest}"
    dest.unlink()
    return f"removido -> {dest}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Instala PEP-Codex para Codex.")
    parser.add_argument("--here", action="store_true", help="instalar no projeto atual")
    parser.add_argument("--path", action="append", metavar="CAMINHO", help="instalar em projeto especifico")
    parser.add_argument("--global", dest="global_scope", action="store_true", help="instalar globalmente")
    parser.add_argument("--legacy-prompt", action="store_true", help="instalar tambem /prompts:pepcodex")
    parser.add_argument("--force", action="store_true", help="forcar atualizacao dos arquivos gerenciados")
    parser.add_argument("--uninstall", action="store_true", help="desinstalar dos alvos")
    args = parser.parse_args()

    scopes = resolve_scopes(args.here, args.path, False)
    if args.global_scope:
        scopes.append(Scope(Path.home() / ".codex", True))
    if not scopes and not args.legacy_prompt:
        parser.print_help()
        return 2
    if not scopes and args.legacy_prompt:
        result = remove_legacy_prompt() if args.uninstall else install_legacy_prompt(args.force)
        print(f"/prompts:pepcodex: {result}")
        print("Uso recomendado: $pepcodex")
        return 0

    results = []
    for scope in scopes:
        if args.uninstall:
            results.append(_PROVIDER.uninstall(scope, legacy_prompt=args.legacy_prompt))
        else:
            results.append(_PROVIDER.install(scope, force=args.force, legacy_prompt=args.legacy_prompt))
    print(format_results(results))
    print("Uso recomendado: $pepcodex")
    if args.legacy_prompt and not args.uninstall:
        print("Compatibilidade: /prompts:pepcodex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
