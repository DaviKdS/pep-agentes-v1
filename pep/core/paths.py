"""Path helpers shared by CLI, GUI and providers."""

from __future__ import annotations

import sys
from pathlib import Path


def package_root() -> Path:
    """Return the project/resource root, supporting PyInstaller onefile."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parents[2]


def user_home() -> Path:
    return Path.home()


def prompt_path(relative: str) -> Path:
    return package_root() / relative
