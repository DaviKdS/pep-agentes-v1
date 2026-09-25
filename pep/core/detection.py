"""Local-only tool detection used by doctor/status."""

from __future__ import annotations

import importlib.util
import platform
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ToolStatus:
    name: str
    found: bool
    detail: str


@dataclass(frozen=True)
class VSCodeExtension:
    extension_id: str
    version: str
    path: Path
    channel: str


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


def vscode_extension_roots(home: Path | None = None) -> list[tuple[str, Path]]:
    """Return known VS Code extension roots for the current user."""

    home = home or Path.home()
    return [
        ("VS Code", home / ".vscode" / "extensions"),
        ("VS Code Insiders", home / ".vscode-insiders" / "extensions"),
    ]


def _version_key(version: str) -> tuple[int, ...]:
    """Convert a numeric dotted version to a sortable tuple."""

    try:
        return tuple(int(part) for part in version.split("."))
    except ValueError:
        return ()


def _extension_version(directory_name: str, extension_id: str) -> str | None:
    """Extract a numeric version from a VS Code extension directory name."""

    pattern = rf"^{re.escape(extension_id)}-(\d+(?:\.\d+)+)(?:-|$)"
    match = re.match(pattern, directory_name, flags=re.IGNORECASE)
    return match.group(1) if match else None


def find_latest_vscode_extension(
    extension_id: str,
    *,
    roots: list[tuple[str, Path]] | None = None,
) -> VSCodeExtension | None:
    """Find the newest installed copy of a VS Code extension by Marketplace ID."""

    candidates: list[VSCodeExtension] = []

    for channel, root in roots or vscode_extension_roots():
        if not root.is_dir():
            continue

        try:
            entries = list(root.iterdir())
        except OSError:
            continue

        for entry in entries:
            if not entry.is_dir():
                continue

            version = _extension_version(entry.name, extension_id)
            if not version:
                continue

            candidates.append(
                VSCodeExtension(
                    extension_id=extension_id,
                    version=version,
                    path=entry,
                    channel=channel,
                )
            )

    if not candidates:
        return None

    return max(candidates, key=lambda item: _version_key(item.version))


def detect_ai_tool(
    *,
    name: str,
    cli_command: str,
    vscode_extension_id: str,
) -> ToolStatus:
    """Detect an AI provider through its CLI, VS Code extension, or both."""

    cli_path = shutil.which(cli_command)
    extension = find_latest_vscode_extension(vscode_extension_id)

    if cli_path and extension:
        return ToolStatus(
            name,
            True,
            f"CLI + {extension.channel} extension {extension.version}",
        )

    if cli_path:
        return ToolStatus(name, True, f"CLI - {cli_path}")

    if extension:
        return ToolStatus(
            name,
            True,
            f"{extension.channel} extension {extension.version}",
        )

    return ToolStatus(
        name,
        False,
        f"CLI '{cli_command}' ou extensao '{vscode_extension_id}' nao encontrados",
    )


def detect_claude() -> ToolStatus:
    return detect_ai_tool(
        name="Claude Code",
        cli_command="claude",
        vscode_extension_id="anthropic.claude-code",
    )


def detect_codex() -> ToolStatus:
    return detect_ai_tool(
        name="Codex",
        cli_command="codex",
        vscode_extension_id="openai.chatgpt",
    )


def doctor_tools() -> list[ToolStatus]:
    return [
        detect_system(),
        detect_python(),
        detect_command("Git", "git"),
        detect_claude(),
        detect_codex(),
        detect_genpyexe(),
    ]
