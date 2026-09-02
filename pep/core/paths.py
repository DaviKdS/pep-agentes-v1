"""Path helpers shared by CLI, GUI and providers."""

from __future__ import annotations

import sys
from pathlib import Path


def package_root() -> Path:
    """Return the project/resource root, supporting PyInstaller onefile."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    source_root = Path(__file__).resolve().parents[2]
    if (source_root / "claude").exists() and (source_root / "codex").exists():
        return source_root
    installed_root = Path(sys.prefix) / "share" / "pep-agentes"
    if installed_root.exists():
        return installed_root
    return source_root


def user_home() -> Path:
    return Path.home()


def prompt_path(relative: str) -> Path:
    return package_root() / relative
