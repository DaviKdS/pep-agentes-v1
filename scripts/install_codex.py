#!/usr/bin/env python3
"""Instala PEP-Codex para Codex em projeto(s) ou globalmente.

Projeto:
  AGENTS.md
  .agents/skills/pepcodex/

Global:
  ~/.codex/AGENTS.md
  ~/.agents/skills/pepcodex/

Compatibilidade opcional:
  ~/.codex/prompts/pepcodex.md -> /prompts:pepcodex

O instalador e idempotente e preserva conteudo fora dos marcadores PEP-CODEX.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

BLOCK_RE = re.compile(
    r"<!-- PEP-CODEX:START.*?<!-- PEP-CODEX:END -->",
    re.DOTALL,
)


def resource_base() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parents[1]


ROOT = resource_base()
SOURCE_AGENTS = ROOT / "codex" / "AGENTS.md"
SOURCE_SKILL = ROOT / "codex" / "skills" / "pepcodex"
SOURCE_PROMPT = ROOT / "codex" / "prompts" / "pepcodex.md"


def read_block() -> str:
    text = SOURCE_AGENTS.read_text(encoding="utf-8")
    match = BLOCK_RE.search(text)
    if not match:
        raise RuntimeError(f"Marcadores PEP-CODEX nao encontrados em {SOURCE_AGENTS}")
    return match.group(0)


def upsert_block(path: Path, block: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if BLOCK_RE.search(current):
            path.write_text(BLOCK_RE.sub(lambda _: block, current), encoding="utf-8")
            return "atualizado"
        sep = "" if current.endswith("\n") else "\n"
        path.write_text(f"{current}{sep}\n{block}\n", encoding="utf-8")
        return "bloco adicionado"
    path.write_text(
        "# Instrucoes do projeto (Codex)\n\n"
        "Bloco PEP-Codex gerenciado por scripts/install_codex.py.\n\n"
        f"{block}\n",
        encoding="utf-8",
    )
    return "criado"


def remove_block(path: Path) -> str:
    if not path.exists():
        return "inexistente"
    current = path.read_text(encoding="utf-8")
    if not BLOCK_RE.search(current):
        return "sem bloco"
    updated = BLOCK_RE.sub("", current).rstrip() + "\n"
    path.write_text(updated, encoding="utf-8")
    return "bloco removido"


def copy_skill(dest: Path, force: bool) -> str:
    if dest.exists():
        if not force:
            return "ja existe (use --force para atualizar)"
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE_SKILL, dest)
    return "instalada"


def remove_skill(dest: Path) -> str:
    if not dest.exists():
        return "inexistente"
    shutil.rmtree(dest)
    return "removida"


def project_targets(project: Path) -> tuple[Path, Path]:
    return project / "AGENTS.md", project / ".agents" / "skills" / "pepcodex"


def global_targets() -> tuple[Path, Path]:
    return Path.home() / ".codex" / "AGENTS.md", Path.home() / ".agents" / "skills" / "pepcodex"


def install_one(label: str, agents: Path, skill: Path, block: str, force: bool) -> None:
    print(f"\n== {label} ==")
    print(f"AGENTS.md: {upsert_block(agents, block)} -> {agents}")
    print(f"$pepcodex: {copy_skill(skill, force)} -> {skill}")


def uninstall_one(label: str, agents: Path, skill: Path) -> None:
    print(f"\n== {label} ==")
    print(f"AGENTS.md: {remove_block(agents)} -> {agents}")
    print(f"$pepcodex: {remove_skill(skill)} -> {skill}")


def install_legacy_prompt(force: bool) -> str:
    dest = Path.home() / ".codex" / "prompts" / "pepcodex.md"
    if dest.exists() and not force:
        return f"ja existe (use --force para atualizar) -> {dest}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_PROMPT, dest)
    return f"instalado -> {dest}"


def remove_legacy_prompt() -> str:
    dest = Path.home() / ".codex" / "prompts" / "pepcodex.md"
    if not dest.exists():
        return f"inexistente -> {dest}"
    dest.unlink()
    return f"removido -> {dest}"


def resolve_targets(args: argparse.Namespace) -> list[tuple[str, Path, Path]]:
    targets: list[tuple[str, Path, Path]] = []
    if args.here:
        agents, skill = project_targets(Path.cwd())
        targets.append((str(Path.cwd()), agents, skill))
    for raw in args.path or []:
        project = Path(raw).expanduser().resolve()
        agents, skill = project_targets(project)
        targets.append((str(project), agents, skill))
    if args.global_scope:
        agents, skill = global_targets()
        targets.append(("GLOBAL", agents, skill))
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description="Instala PEP-Codex para Codex.")
    parser.add_argument("--here", action="store_true", help="instalar no projeto atual")
    parser.add_argument("--path", action="append", metavar="CAMINHO", help="instalar em projeto especifico")
    parser.add_argument("--global", dest="global_scope", action="store_true", help="instalar globalmente")
    parser.add_argument(
        "--legacy-prompt",
        action="store_true",
        help="instalar tambem /prompts:pepcodex (recurso legado/depreciado)",
    )
    parser.add_argument("--force", action="store_true", help="forcar atualizacao dos arquivos gerenciados")
    parser.add_argument("--uninstall", action="store_true", help="desinstalar dos alvos")
    args = parser.parse_args()

    targets = resolve_targets(args)
    if not targets and not args.legacy_prompt:
        parser.print_help()
        return 2

    block = read_block()
    for label, agents, skill in targets:
        if args.uninstall:
            uninstall_one(label, agents, skill)
        else:
            install_one(label, agents, skill, block, args.force)

    if args.legacy_prompt:
        result = remove_legacy_prompt() if args.uninstall else install_legacy_prompt(args.force)
        print(f"\n/prompts:pepcodex: {result}")

    print("\nConcluido.")
    print("Uso recomendado: $pepcodex")
    if args.legacy_prompt and not args.uninstall:
        print("Compatibilidade: /prompts:pepcodex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
