#!/usr/bin/env python3
"""Update the full portable prompt from a local text file.

Usage:
    python scripts/update_prompt.py caminho/do/novo_prompt.txt

This script only reads the provided local file and overwrites
prompts/pep-agentes-completo.txt after basic validation.
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / "prompts" / "pep-agentes-completo.txt"

MIN_LENGTH = 200


def update_prompt(source: Path) -> None:
    """Replace the full prompt with the content from source."""
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {source}")

    content = source.read_text(encoding="utf-8").strip()
    if len(content) < MIN_LENGTH:
        raise ValueError("O novo prompt parece curto demais para substituir o prompt completo.")

    TARGET.write_text(content + "\n", encoding="utf-8")
    print(f"Prompt atualizado: {TARGET}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    update_prompt(Path(sys.argv[1]).resolve())
