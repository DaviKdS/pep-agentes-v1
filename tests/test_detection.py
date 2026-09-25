from __future__ import annotations

from pathlib import Path

from pep.core import detection


def test_find_latest_vscode_extension_prefers_newest_version(tmp_path):
    root = tmp_path / ".vscode" / "extensions"
    root.mkdir(parents=True)

    (root / "anthropic.claude-code-2.1.281-win32-x64").mkdir()
    (root / "anthropic.claude-code-2.1.282-win32-x64").mkdir()

    result = detection.find_latest_vscode_extension(
        "anthropic.claude-code",
        roots=[("VS Code", root)],
    )

    assert result is not None
    assert result.version == "2.1.282"
    assert result.path.name == "anthropic.claude-code-2.1.282-win32-x64"
    assert result.channel == "VS Code"


def test_find_latest_vscode_extension_detects_codex(tmp_path):
    root = tmp_path / ".vscode" / "extensions"
    root.mkdir(parents=True)
    (root / "openai.chatgpt-26.5917.62051-win32-x64").mkdir()

    result = detection.find_latest_vscode_extension(
        "openai.chatgpt",
        roots=[("VS Code", root)],
    )

    assert result is not None
    assert result.version == "26.5917.62051"


def test_detect_ai_tool_accepts_extension_without_cli(monkeypatch):
    extension = detection.VSCodeExtension(
        extension_id="openai.chatgpt",
        version="26.5917.62051",
        path=Path("openai.chatgpt-26.5917.62051-win32-x64"),
        channel="VS Code",
    )

    monkeypatch.setattr(detection.shutil, "which", lambda command: None)
    monkeypatch.setattr(
        detection,
        "find_latest_vscode_extension",
        lambda extension_id: extension,
    )

    status = detection.detect_codex()

    assert status.found is True
    assert status.name == "Codex"
    assert status.detail == "VS Code extension 26.5917.62051"


def test_detect_ai_tool_reports_cli_and_extension(monkeypatch):
    extension = detection.VSCodeExtension(
        extension_id="anthropic.claude-code",
        version="2.1.282",
        path=Path("anthropic.claude-code-2.1.282-win32-x64"),
        channel="VS Code",
    )

    monkeypatch.setattr(
        detection.shutil,
        "which",
        lambda command: "C:/Tools/claude.exe" if command == "claude" else None,
    )
    monkeypatch.setattr(
        detection,
        "find_latest_vscode_extension",
        lambda extension_id: extension,
    )

    status = detection.detect_claude()

    assert status.found is True
    assert status.detail == "CLI + VS Code extension 2.1.282"


def test_detect_ai_tool_fails_only_when_cli_and_extension_are_absent(monkeypatch):
    monkeypatch.setattr(detection.shutil, "which", lambda command: None)
    monkeypatch.setattr(
        detection,
        "find_latest_vscode_extension",
        lambda extension_id: None,
    )

    status = detection.detect_codex()

    assert status.found is False
    assert "openai.chatgpt" in status.detail
