#!/usr/bin/env python3
"""Wrapper de compatibilidade para o build Windows.

O backend preferencial agora e o GenPyEXE em scripts/build_windows.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_windows import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
