#!/usr/bin/env python3
"""Instala o protocolo PEP-Agentes v1.0 para o Claude Code no escopo escolhido.

Escopos:
    - este projeto (diretorio atual):   --here
    - projetos especificos (1+ paths):  --path CAMINHO  (pode repetir)
    - global (~/.claude):               --global
    - sem argumentos:                   modo interativo (pergunta o escopo)

O que e instalado em cada alvo:
    - CLAUDE.md  -> bloco PEP-Agentes gerenciado por marcadores (idempotente,
      preserva o resto do arquivo se ja existir).
    - .claude/commands/pep.md  -> comando /pep.

Este script apenas escreve arquivos locais. Nao envia dados, nao le credenciais
e nao coleta informacoes pessoais.

Exemplos:
    python scripts/install_claude.py --here
    python scripts/install_claude.py --global
    python scripts/install_claude.py --path "C:/projetos/loja" --path "C:/projetos/api"
    python scripts/install_claude.py --uninstall --here
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

def _resource_base() -> Path:
    """Base dos arquivos-fonte (claude/...), tanto rodando como .py quanto no .exe."""
    if getattr(sys, "frozen", False):
        # Empacotado pelo PyInstaller: recursos ficam em sys._MEIPASS.
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parents[1]


PACKAGE_ROOT = _resource_base()
SOURCE_CLAUDE_MD = PACKAGE_ROOT / "claude" / "CLAUDE.md"
SOURCE_COMMAND = PACKAGE_ROOT / "claude" / "commands" / "pep.md"

BLOCK_RE = re.compile(
    r"<!-- PEP-AGENTES:START.*?<!-- PEP-AGENTES:END -->",
    re.DOTALL,
)

NEW_FILE_HEADER = (
    "# Instrucoes do projeto (Claude Code)\n\n"
    "Bloco PEP-Agentes gerenciado por scripts/install_claude.py (nao edite entre os marcadores).\n\n"
)


def read_block() -> str:
    """Extrai o bloco PEP (com marcadores) da fonte canonica."""
    text = SOURCE_CLAUDE_MD.read_text(encoding="utf-8")
    match = BLOCK_RE.search(text)
    if not match:
        raise RuntimeError(f"Marcadores PEP nao encontrados em {SOURCE_CLAUDE_MD}")
    return match.group(0)


def upsert_block(claude_md: Path, block: str) -> str:
    """Cria/atualiza o bloco PEP em um CLAUDE.md, preservando o restante."""
    if claude_md.exists():
        current = claude_md.read_text(encoding="utf-8")
        if BLOCK_RE.search(current):
            updated = BLOCK_RE.sub(lambda _: block, current)
            action = "atualizado"
        else:
            sep = "" if current.endswith("\n") else "\n"
            updated = f"{current}{sep}\n{block}\n"
            action = "bloco adicionado"
    else:
        claude_md.parent.mkdir(parents=True, exist_ok=True)
        updated = f"{NEW_FILE_HEADER}{block}\n"
        action = "criado"
    claude_md.write_text(updated, encoding="utf-8")
    return action


def remove_block(claude_md: Path) -> str:
    """Remove o bloco PEP de um CLAUDE.md, se existir."""
    if not claude_md.exists():
        return "inexistente"
    current = claude_md.read_text(encoding="utf-8")
    if not BLOCK_RE.search(current):
        return "sem bloco"
    updated = BLOCK_RE.sub("", current).rstrip() + "\n"
    claude_md.write_text(updated, encoding="utf-8")
    return "bloco removido"


def targets_for(scope_dir: Path, is_global: bool) -> tuple[Path, Path]:
    """Retorna (caminho do CLAUDE.md, caminho do comando pep.md)."""
    if is_global:
        base = scope_dir  # ~/.claude
        return base / "CLAUDE.md", base / "commands" / "pep.md"
    return scope_dir / "CLAUDE.md", scope_dir / ".claude" / "commands" / "pep.md"


def install_target(scope_dir: Path, block: str, command_text: str,
                   is_global: bool, force: bool) -> None:
    claude_md, command_path = targets_for(scope_dir, is_global)

    action = upsert_block(claude_md, block)
    print(f"  CLAUDE.md: {action} -> {claude_md}")

    command_path.parent.mkdir(parents=True, exist_ok=True)
    if command_path.exists() and not force:
        if command_path.read_text(encoding="utf-8") == command_text:
            print(f"  /pep: ja atualizado -> {command_path}")
        else:
            print(f"  /pep: JA EXISTE (use --force para sobrescrever) -> {command_path}")
    else:
        command_path.write_text(command_text, encoding="utf-8")
        print(f"  /pep: instalado -> {command_path}")


def uninstall_target(scope_dir: Path, is_global: bool) -> None:
    claude_md, command_path = targets_for(scope_dir, is_global)
    print(f"  CLAUDE.md: {remove_block(claude_md)} -> {claude_md}")
    if command_path.exists():
        command_path.unlink()
        print(f"  /pep: removido -> {command_path}")
    else:
        print(f"  /pep: inexistente -> {command_path}")


def resolve_scopes(args: argparse.Namespace) -> list[tuple[Path, bool]]:
    """Monta a lista de (diretorio, is_global) a partir dos argumentos/interativo."""
    scopes: list[tuple[Path, bool]] = []
    if args.here:
        scopes.append((Path.cwd(), False))
    for p in args.path or []:
        scopes.append((Path(p).expanduser().resolve(), False))
    if getattr(args, "global"):
        scopes.append((Path.home() / ".claude", True))

    if scopes:
        return scopes
    return interactive_scopes()


def interactive_scopes() -> list[tuple[Path, bool]]:
    print("Onde instalar o PEP-Agentes para o Claude Code?")
    print("  1) So este projeto (diretorio atual)")
    print("  2) Projetos especificos (informe os caminhos)")
    print("  3) Global (~/.claude, vale para todos os projetos)")
    choice = input("Escolha [1/2/3]: ").strip()
    if choice == "1":
        return [(Path.cwd(), False)]
    if choice == "2":
        raw = input("Caminhos separados por virgula: ").strip()
        paths = [p.strip() for p in raw.split(",") if p.strip()]
        return [(Path(p).expanduser().resolve(), False) for p in paths]
    if choice == "3":
        return [(Path.home() / ".claude", True)]
    print("Opcao invalida.")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Instala o PEP-Agentes v1.0 para o Claude Code.")
    parser.add_argument("--here", action="store_true", help="instalar no diretorio atual")
    parser.add_argument("--path", action="append", metavar="CAMINHO",
                        help="instalar em um projeto especifico (pode repetir)")
    parser.add_argument("--global", action="store_true", help="instalar em ~/.claude")
    parser.add_argument("--force", action="store_true", help="sobrescrever pep.md existente")
    parser.add_argument("--uninstall", action="store_true", help="remover o PEP dos alvos")
    args = parser.parse_args()

    scopes = resolve_scopes(args)
    if not scopes:
        print("Nenhum alvo selecionado.")
        return 2

    block = read_block()
    command_text = SOURCE_COMMAND.read_text(encoding="utf-8")

    for scope_dir, is_global in scopes:
        label = "GLOBAL" if is_global else str(scope_dir)
        print(f"\n== {label} ==")
        if args.uninstall:
            uninstall_target(scope_dir, is_global)
        else:
            install_target(scope_dir, block, command_text, is_global, args.force)

    print("\nConcluido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
