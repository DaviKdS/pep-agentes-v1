"""Local-only tool detection used by doctor/status."""

from __future__ import annotations

import importlib.util
import platform
import shutil
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class ToolStatus:
    name: str
    found: bool
    detail: str


def detect_command(name: str, command: str) -> ToolStatus:
    path = shutil.which(command)
    return ToolStatus(name, bool(path), path or "nao encontrado no PATH")


def detect_python() -> ToolStatus:
    return ToolStatus("Python", True, sys.version.split()[0])


def detect_system() -> ToolStatus:
    return ToolStatus("Sistema", True, f"{platform.system()} {platform.release()}".strip())


def detect_genpyexe() -> ToolStatus:
    if importlib.util.find_spec("genpyexeks"):
        return ToolStatus("GenPyEXE", True, "modulo genpyexeks disponivel")
    path = shutil.which("genpyexe")
    return ToolStatus("GenPyEXE", bool(path), path or "instale com: pip install genpyexe")


def doctor_tools() -> list[ToolStatus]:
    return [
        detect_system(),
        detect_python(),
        detect_command("Git", "git"),
        detect_command("Claude Code", "claude"),
        detect_command("Codex", "codex"),
        detect_genpyexe(),
    ]
