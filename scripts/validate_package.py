#!/usr/bin/env python3
"""Validate the expected package structure.

This script checks local files only. It does not transmit data anywhere.
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "COMO_USAR.md",
    "CHANGELOG.md",
    "SECURITY.md",
    ".gitignore",
    ".github/workflows/ci.yml",
    ".github/workflows/python-package.yml",
    ".github/workflows/release.yml",
    ".env.example",
    "manifest.json",
    "pyproject.toml",
    "MANIFEST.in",
    "requirements.txt",
    "prompts/pep-agentes-completo.txt",
    "prompts/pep-agentes-curto.txt",
    "prompts/pep-agentes-claude.txt",
    "docs/documentacao.pdf",
    "docs/COMO_FOI_GERADO.md",
    "docs/PEP-CODEX.md",
    "claude/CLAUDE.md",
    "claude/commands/pep.md",
    "codex/AGENTS.md",
    "codex/prompts/pepcodex.md",
    "codex/skills/pepcodex/SKILL.md",
    "codex/skills/pepcodex/agents/openai.yaml",
    "codex/skills/pepcodex/references/PROTOCOLO.md",
    "codex/skills/pepcodex/tools/context_eco.py",
    "requirements-app.txt",
    "requirements-build.txt",
    "genpyexe.toml",
    "pep/__init__.py",
    "pep/core/version.py",
    "pep/core/markers.py",
    "pep/core/detection.py",
    "pep/providers/claude.py",
    "pep/providers/codex.py",
    "pep/services/manager.py",
    "scripts/pep.py",
    "scripts/__init__.py",
    "scripts/build_zip.py",
    "scripts/generate_documentation_pdf.py",
    "scripts/validate_package.py",
    "scripts/update_prompt.py",
    "scripts/install_claude.py",
    "scripts/install_codex.py",
    "scripts/pep_gui.py",
    "scripts/build_app.py",
    "scripts/build_windows.py",
    "scripts/publish_github.sh",
    "scripts/publish_github.ps1",
    "installer/install_app.ps1",
    "installer/uninstall_app.ps1",
    "installer/PEP-Agentes.iss",
    "tests/test_markers.py",
    "tests/test_providers.py",
    "tests/test_cli.py",
    "tests/conftest.py",
]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (PROJECT_ROOT / path).exists()]
    if missing:
        print("Arquivos ausentes:")
        for path in missing:
            print(f"- {path}")
        return 1

    print("Pacote validado com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
