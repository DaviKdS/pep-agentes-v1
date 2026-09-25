"""Path helpers shared by CLI, GUI and providers."""

from __future__ import annotations

import sys
from pathlib import Path


def package_root() -> Path:
    """Return the runtime resource root, supporting wheels and PyInstaller onefile."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))

    package_dir = Path(__file__).resolve().parents[1]
    packaged_resources = package_dir / "resources"
    if packaged_resources.exists():
        return packaged_resources

    # Development/source-tree compatibility for older checkouts.
    source_root = Path(__file__).resolve().parents[2]
    if (source_root / "claude").exists() and (source_root / "codex").exists():
        return source_root

    return packaged_resources


def user_home() -> Path:
    return Path.home()


def prompt_path(relative: str) -> Path:
    return package_root() / relative
