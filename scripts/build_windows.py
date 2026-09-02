#!/usr/bin/env python3
"""Build Windows artifacts with GenPyEXE.

GenPyEXE is intentionally imported only in this build script. The PEP Manager
runtime does not depend on GenPyEXE.
"""

from __future__ import annotations

import hashlib
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pep.core.version import APP_NAME, __version__  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST = PROJECT_ROOT / "dist"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_versioned(source: Path, dest_name: str) -> Path:
    dest = DIST / dest_name
    if source.resolve() != dest.resolve():
        shutil.copy2(source, dest)
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Windows artifacts with GenPyEXE.")
    parser.add_argument("--dry-run", action="store_true", help="validate configuration without building")
    args = parser.parse_args()
    if args.dry_run:
        print(f"Projeto: {PROJECT_ROOT}")
        print(f"App: {APP_NAME} {__version__}")
        print("Backend: GenPyEXE")
        return 0

    try:
        import genpyexeks
        from genpyexeks import InstallerOptions
    except ImportError:
        print("GenPyEXE nao encontrado. Instale com: python -m pip install -r requirements-build.txt")
        return 1

    DIST.mkdir(exist_ok=True)
    result = genpyexeks.build(
        PROJECT_ROOT,
        app_name=APP_NAME,
        version=__version__,
        publisher="DaviKdS",
        description="Gerenciador do protocolo PEP-Agentes para Claude Code e Codex",
        entrypoint=PROJECT_ROOT / "scripts" / "pep_gui.py",
        onefile=True,
        windowed=True,
        isolated=True,
        installer=InstallerOptions(
            desktop_shortcut=True,
            start_menu=True,
            launch_after_install=True,
            per_user_install=True,
            add_to_path=False,
        ),
        output_dir=DIST,
        collect_all=["customtkinter"],
        extra_data=[
            (str(PROJECT_ROOT / "claude"), "claude"),
            (str(PROJECT_ROOT / "codex"), "codex"),
            (str(PROJECT_ROOT / "prompts"), "prompts"),
            (str(PROJECT_ROOT / "docs"), "docs"),
        ],
        clean=True,
    )

    artifacts: list[Path] = []
    if result.exe_path:
        artifacts.append(copy_versioned(Path(result.exe_path), f"{APP_NAME}-{__version__}-Portable-x64.exe"))
    if result.installer_path:
        artifacts.append(copy_versioned(Path(result.installer_path), f"{APP_NAME}-{__version__}-Setup-x64.exe"))

    sums = DIST / f"{APP_NAME}-{__version__}-SHA256SUMS.txt"
    sums.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in artifacts),
        encoding="utf-8",
    )
    artifacts.append(sums)

    print("Artefatos gerados:")
    for path in artifacts:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
