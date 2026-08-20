#!/usr/bin/env python3
"""PEP-Codex context economy helper.

Localiza stack e arquivos candidatos sem despejar o repositorio inteiro no prompt.
Nao envia dados para rede e nao le credenciais por intencao.
"""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".next",
    ".nuxt",
    ".turbo",
    "node_modules",
    "dist",
    "build",
    "out",
    "coverage",
    "target",
    "vendor",
    ".gradle",
    ".idea",
    ".vscode",
}

MANIFESTS = [
    "AGENTS.md",
    "package.json",
    "tsconfig.json",
    "vite.config.ts",
    "vite.config.js",
    "next.config.js",
    "next.config.mjs",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "Pipfile",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "composer.json",
    "Gemfile",
    "pubspec.yaml",
    "Package.swift",
    "CMakeLists.txt",
    "Makefile",
    "meson.build",
    "platformio.ini",
    "sdkconfig",
    "Dockerfile",
    "compose.yml",
    "docker-compose.yml",
    "terraform.tf",
    "nx.json",
    "turbo.json",
    "pnpm-workspace.yaml",
]

LOCK_HINTS = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "poetry.lock",
    "Pipfile.lock",
    "Cargo.lock",
    "go.sum",
    "composer.lock",
    "Gemfile.lock",
}

TEXT_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".css",
    ".go",
    ".h",
    ".hpp",
    ".html",
    ".java",
    ".js",
    ".jsx",
    ".json",
    ".kt",
    ".md",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".swift",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(root):
        current_path = Path(current)
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        if is_excluded(current_path.relative_to(root)):
            continue
        for name in names:
            p = current_path / name
            if p.is_file():
                files.append(p)
    return files


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def detect_stack(root: Path, files: list[Path]) -> list[str]:
    names = {p.name for p in files}
    rels = {rel(root, p) for p in files}
    stack: list[str] = []

    def add(label: str) -> None:
        if label not in stack:
            stack.append(label)

    if "package.json" in names:
        add("JavaScript/TypeScript")
    if {"pyproject.toml", "requirements.txt", "setup.py", "Pipfile"} & names:
        add("Python")
    if "Cargo.toml" in names:
        add("Rust")
    if "go.mod" in names:
        add("Go")
    if {"pom.xml", "build.gradle", "settings.gradle"} & names:
        add("Java/Kotlin")
    if any(p.endswith(".csproj") or p.endswith(".sln") for p in rels):
        add(".NET")
    if "composer.json" in names:
        add("PHP")
    if "Gemfile" in names:
        add("Ruby")
    if "pubspec.yaml" in names:
        add("Flutter/Dart")
    if "Package.swift" in names or any(".xcodeproj/" in p or ".xcworkspace/" in p for p in rels):
        add("Swift/iOS")
    if {"CMakeLists.txt", "Makefile", "meson.build"} & names:
        add("C/C++")
    if {"platformio.ini", "sdkconfig"} & names:
        add("Embedded")
    if {"Dockerfile", "compose.yml", "docker-compose.yml", "terraform.tf"} & names:
        add("Infra")
    if {"pnpm-workspace.yaml", "turbo.json", "nx.json"} & names:
        add("Monorepo")
    return stack


def task_terms(task: str) -> list[str]:
    raw = re.findall(r"[A-Za-z0-9_\-./]{3,}", task.lower())
    stop = {"mode", "eco", "full", "plan", "debug", "review", "bootstrap", "corrigir", "criar"}
    terms = []
    for item in raw:
        item = item.strip("./")
        if item and item not in stop and item not in terms:
            terms.append(item)
    return terms[:12]


def is_probably_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in MANIFESTS or path.name.startswith(".env")


def file_mentions_terms(path: Path, terms: list[str]) -> bool:
    if not terms:
        return False
    lower_rel = path.as_posix().lower()
    if any(term in lower_rel for term in terms):
        return True
    if not is_probably_text(path):
        return False
    try:
        if path.stat().st_size > 256_000:
            return False
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return False
    return any(term in text for term in terms)


def ranked_candidates(root: Path, files: list[Path], task: str, limit: int) -> list[str]:
    terms = task_terms(task)
    scored: list[tuple[int, str]] = []
    for path in files:
        relative = rel(root, path)
        name = path.name
        score = 0
        if name in MANIFESTS:
            score += 30
        if name in {"AGENTS.md", "README.md"}:
            score += 20
        if path.suffix.lower() in {".test.ts", ".spec.ts", ".test.js", ".spec.js"}:
            score += 8
        if file_mentions_terms(path, terms):
            score += 60
        if name in LOCK_HINTS:
            score -= 20
        if relative.startswith(("docs/", "doc/")):
            score -= 8
        if score > 0:
            scored.append((score, relative))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [item[1] for item in scored[:limit]]


def agent_files(root: Path, files: list[Path]) -> list[str]:
    return [rel(root, p) for p in files if p.name in {"AGENTS.md", "AGENTS.override.md"}][:12]


def manifests(root: Path, files: list[Path]) -> list[str]:
    return [rel(root, p) for p in files if p.name in MANIFESTS or p.name in LOCK_HINTS][:40]


def state_excerpt(root: Path) -> str:
    path = root / ".pepcodex" / "state.md"
    if not path.exists():
        return "(sem checkpoint)"
    try:
        return "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:30])
    except OSError as exc:
        return f"(erro ao ler checkpoint: {exc})"


def scan(root: Path, task: str, limit: int) -> str:
    files = iter_files(root)
    stacks = detect_stack(root, files)
    lines = [
        "# PEP-Codex ECO Context",
        f"root: {root}",
        f"task: {task or '-'}",
        f"stack: {', '.join(stacks) if stacks else 'nao identificada'}",
        "",
        "## checkpoint",
        state_excerpt(root),
        "",
        "## AGENTS aplicaveis/candidatos",
    ]
    agents = agent_files(root, files)
    lines.extend(f"- {p}" for p in agents) if agents else lines.append("- nenhum")
    lines.extend(["", "## manifests/configs (leia so os necessarios)"])
    mfiles = manifests(root, files)
    lines.extend(f"- {p}" for p in mfiles) if mfiles else lines.append("- nenhum reconhecido")
    lines.extend(["", "## arquivos candidatos"])
    candidates = ranked_candidates(root, files, task, limit)
    lines.extend(f"- {p}" for p in candidates) if candidates else lines.append("- nenhum candidato por termo")
    lines.extend(
        [
            "",
            "Regra: abra primeiro os candidatos diretamente ligados a tarefa e seus testes.",
            "Lockfiles acima sao apenas sinalizadores de gerenciador; nao carregue conteudo sem necessidade.",
        ]
    )
    return "\n".join(lines)


def checkpoint(root: Path, args: argparse.Namespace) -> Path:
    target_dir = root / ".pepcodex"
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / "state.md"
    rows = [
        "# PEP-Codex State",
        f"Objetivo: {args.goal or '-'}",
        f"Stack: {args.stack or '-'}",
        f"Status: {args.status or '-'}",
        f"Ultima mudanca: {args.change or '-'}",
        f"Arquivos-chave: {args.files or '-'}",
        f"Validacao: {args.validation or '-'}",
        f"Bloqueios: {args.blockers or '-'}",
        f"Proximo: {args.next or '-'}",
        f"Decisoes: {args.decisions or '-'}",
    ]
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="PEP-Codex helper de contexto economico.")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_parser = sub.add_parser("scan", help="listar contexto candidato para uma tarefa")
    scan_parser.add_argument("--root", default=".", help="raiz do repositorio/projeto")
    scan_parser.add_argument("--task", default="", help="pedido atual")
    scan_parser.add_argument("--limit", type=int, default=12, help="limite de arquivos candidatos")

    chk = sub.add_parser("checkpoint", help="gravar .pepcodex/state.md curto")
    chk.add_argument("--root", default=".", help="raiz do repositorio/projeto")
    chk.add_argument("--goal", default="")
    chk.add_argument("--stack", default="")
    chk.add_argument("--status", default="")
    chk.add_argument("--change", default="")
    chk.add_argument("--files", default="")
    chk.add_argument("--validation", default="")
    chk.add_argument("--blockers", default="")
    chk.add_argument("--next", default="")
    chk.add_argument("--decisions", default="")

    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if args.command == "scan":
        print(scan(root, args.task, max(1, min(args.limit, 30))))
        return 0

    path = checkpoint(root, args)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
