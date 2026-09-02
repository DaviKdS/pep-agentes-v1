#!/usr/bin/env python3
"""Build a ZIP package from the current project folder.

This script is intentionally local-only: it does not upload files, does not
read credentials, and does not collect personal data.
"""
from __future__ import annotations

import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ZIP_NAME = f"{PROJECT_ROOT.name}.zip"
OUTPUT_DIR = PROJECT_ROOT / "output"
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    ".genpyexe",
    "output",
    "build",
    "dist",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}
EXCLUDE_NAMES = {
    "PROMPT_MESTRE_PEP_AGENTES_ATUALIZACAO.md",
    "PROMPT_MESTRE_PEP_AGENTES_ATUALIZACAO.docx",
    "package.json",
    "package-lock.json",
}


def should_include(path: Path) -> bool:
    """Return True when a file should be included in the package."""
    parts = set(path.relative_to(PROJECT_ROOT).parts)
    if parts & EXCLUDE_DIRS:
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    if path.name in {ZIP_NAME} | EXCLUDE_NAMES:
        return False
    return path.is_file()


def build_zip() -> Path:
    """Create a ZIP archive containing the project files."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    zip_path = OUTPUT_DIR / ZIP_NAME

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(PROJECT_ROOT.rglob("*")):
            if should_include(file_path):
                archive.write(file_path, file_path.relative_to(PROJECT_ROOT.parent))

    return zip_path


if __name__ == "__main__":
    result = build_zip()
    print(f"ZIP criado: {result}")
