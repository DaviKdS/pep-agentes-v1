#!/usr/bin/env python3
"""Empacota a GUI (scripts/pep_gui.py) em um executavel .exe com PyInstaller.

Uso (recomendado com o Python que tem customtkinter + pyinstaller):
    D:/python.exe scripts/build_app.py

Gera:
    dist/PEP-Agentes.exe   (onefile, sem console)

Depois, para instalar no PC, rode:
    powershell -ExecutionPolicy Bypass -File installer/install_app.ps1
Ou, se tiver Inno Setup, este script tenta compilar installer/PEP-Agentes.iss.

Local-only: nao envia dados nem le credenciais.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENTRY = PROJECT_ROOT / "scripts" / "pep_gui.py"
APP_NAME = "PEP-Agentes"
SEP = os.pathsep  # ';' no Windows

DATA = [
    (PROJECT_ROOT / "claude", "claude"),
    (PROJECT_ROOT / "prompts", "prompts"),
]


def build_exe() -> Path:
    try:
        import PyInstaller.__main__ as pyi
    except ImportError:
        print("PyInstaller nao encontrado. Instale com: python -m pip install pyinstaller")
        raise SystemExit(1)

    args = [
        str(ENTRY),
        "--name", APP_NAME,
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--collect-all", "customtkinter",
        "--distpath", str(PROJECT_ROOT / "dist"),
        "--workpath", str(PROJECT_ROOT / "build"),
        "--specpath", str(PROJECT_ROOT / "build"),
    ]
    for src, dest in DATA:
        args += ["--add-data", f"{src}{SEP}{dest}"]

    print("PyInstaller args:\n  " + "\n  ".join(args))
    pyi.run(args)

    exe = PROJECT_ROOT / "dist" / f"{APP_NAME}.exe"
    if not exe.exists():
        print("Falha: exe nao gerado.")
        raise SystemExit(1)
    print(f"\nEXE gerado: {exe}")
    return exe


def try_build_installer() -> None:
    iss = PROJECT_ROOT / "installer" / "PEP-Agentes.iss"
    iscc = shutil.which("iscc") or shutil.which("ISCC")
    for candidate in (
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ):
        if not iscc and Path(candidate).exists():
            iscc = candidate
    if not iscc or not iss.exists():
        print(
            "\nInno Setup nao encontrado (ou .iss ausente): pulei o setup.exe.\n"
            "Para instalar no PC agora, rode:\n"
            "  powershell -ExecutionPolicy Bypass -File installer/install_app.ps1"
        )
        return
    print(f"\nCompilando instalador com Inno Setup: {iscc}")
    subprocess.run([iscc, str(iss)], check=True)
    print("Instalador (setup.exe) gerado em installer/Output/.")


if __name__ == "__main__":
    if sys.platform != "win32":
        print("Aviso: este build foi pensado para Windows (.exe).")
    build_exe()
    try_build_installer()
    print("\nPronto.")
