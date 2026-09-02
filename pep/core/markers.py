"""Marker-managed Markdown block operations."""

from __future__ import annotations

import re
from pathlib import Path


class MarkerError(RuntimeError):
    """Raised when a managed marker block is malformed."""


def _has_broken_markers(text: str, start: str, end: str, pattern: re.Pattern[str]) -> bool:
    starts = text.count(start)
    ends = text.count(end)
    if starts != ends:
        return True
    return starts > 0 and not pattern.search(text)


def read_managed_block(source: Path, pattern: re.Pattern[str]) -> str:
    text = source.read_text(encoding="utf-8")
    match = pattern.search(text)
    if not match:
        raise MarkerError(f"Marcadores PEP nao encontrados em {source}")
    return match.group(0)


def upsert_block(path: Path, block: str, pattern: re.Pattern[str], start: str, end: str, header: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if _has_broken_markers(current, start, end, pattern):
            raise MarkerError(f"Markers corrompidos em {path}")
        if pattern.search(current):
            path.write_text(pattern.sub(lambda _: block, current), encoding="utf-8")
            return "atualizado"
        sep = "" if current.endswith("\n") else "\n"
        path.write_text(f"{current}{sep}\n{block}\n", encoding="utf-8")
        return "bloco adicionado"
    path.write_text(f"{header}{block}\n", encoding="utf-8")
    return "criado"


def remove_block(path: Path, pattern: re.Pattern[str], start: str, end: str) -> str:
    if not path.exists():
        return "inexistente"
    current = path.read_text(encoding="utf-8")
    if _has_broken_markers(current, start, end, pattern):
        raise MarkerError(f"Markers corrompidos em {path}")
    if not pattern.search(current):
        return "sem bloco"
    path.write_text(pattern.sub("", current).rstrip() + "\n", encoding="utf-8")
    return "bloco removido"


def block_state(path: Path, expected: str, pattern: re.Pattern[str], start: str, end: str) -> str:
    if not path.exists():
        return "missing"
    current = path.read_text(encoding="utf-8")
    if _has_broken_markers(current, start, end, pattern):
        return "corrupt"
    match = pattern.search(current)
    if not match:
        return "missing"
    return "current" if match.group(0) == expected else "outdated"
