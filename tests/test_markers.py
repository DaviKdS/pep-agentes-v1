from __future__ import annotations

import re

import pytest

from pep.core.markers import MarkerError, block_state, remove_block, upsert_block

START = "<!-- TEST:START"
END = "<!-- TEST:END -->"
PATTERN = re.compile(r"<!-- TEST:START.*?<!-- TEST:END -->", re.DOTALL)
BLOCK = "<!-- TEST:START -->\nnovo\n<!-- TEST:END -->"
HEADER = "# Header\n\n"


def test_upsert_creates_file(tmp_path):
    target = tmp_path / "AGENTS.md"
    assert upsert_block(target, BLOCK, PATTERN, START, END, HEADER) == "criado"
    assert target.read_text(encoding="utf-8") == f"{HEADER}{BLOCK}\n"


def test_upsert_preserves_manual_content(tmp_path):
    target = tmp_path / "AGENTS.md"
    target.write_text("manual\n", encoding="utf-8")
    assert upsert_block(target, BLOCK, PATTERN, START, END, HEADER) == "bloco adicionado"
    assert target.read_text(encoding="utf-8").startswith("manual\n")


def test_upsert_updates_existing_block(tmp_path):
    target = tmp_path / "AGENTS.md"
    target.write_text("a\n<!-- TEST:START -->\nantigo\n<!-- TEST:END -->\nz\n", encoding="utf-8")
    assert upsert_block(target, BLOCK, PATTERN, START, END, HEADER) == "atualizado"
    assert "antigo" not in target.read_text(encoding="utf-8")


def test_remove_block_preserves_external_content(tmp_path):
    target = tmp_path / "AGENTS.md"
    target.write_text(f"antes\n{BLOCK}\ndepois\n", encoding="utf-8")
    assert remove_block(target, PATTERN, START, END) == "bloco removido"
    assert target.read_text(encoding="utf-8") == "antes\n\ndepois\n"


def test_corrupt_marker_is_detected(tmp_path):
    target = tmp_path / "AGENTS.md"
    target.write_text("antes\n<!-- TEST:START -->\nsem fim\n", encoding="utf-8")
    assert block_state(target, BLOCK, PATTERN, START, END) == "corrupt"
    with pytest.raises(MarkerError):
        upsert_block(target, BLOCK, PATTERN, START, END, HEADER)
