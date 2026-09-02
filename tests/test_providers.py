from __future__ import annotations

from pep.core.models import InstallState, Scope
from pep.providers.claude import ClaudeProvider
from pep.providers.codex import CodexProvider


def test_claude_here_install_status_uninstall(tmp_path):
    provider = ClaudeProvider()
    scope = Scope(tmp_path, False)

    installed = provider.install(scope)
    assert any("CLAUDE.md" in line for line in installed.messages)
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".claude" / "commands" / "pep.md").exists()
    assert provider.status(scope).state == InstallState.CURRENT

    provider.uninstall(scope)
    assert provider.status(scope).state == InstallState.NOT_INSTALLED


def test_codex_here_install_with_legacy_status_uninstall(tmp_path, monkeypatch):
    home = tmp_path / "home"
    monkeypatch.setattr("pep.providers.codex.paths.user_home", lambda: home)
    provider = CodexProvider()
    scope = Scope(tmp_path / "project", False)

    provider.install(scope, legacy_prompt=True)
    assert (scope.path / "AGENTS.md").exists()
    assert (scope.path / ".agents" / "skills" / "pepcodex" / "SKILL.md").exists()
    assert (home / ".codex" / "prompts" / "pepcodex.md").exists()
    assert provider.status(scope, legacy_prompt=True).state == InstallState.CURRENT

    provider.uninstall(scope, legacy_prompt=True)
    assert provider.status(scope, legacy_prompt=True).state == InstallState.NOT_INSTALLED


def test_codex_repair_recreates_missing_skill(tmp_path):
    provider = CodexProvider()
    scope = Scope(tmp_path, False)
    provider.install(scope)
    skill = tmp_path / ".agents" / "skills" / "pepcodex"
    for path in sorted(skill.rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        else:
            path.rmdir()

    assert provider.status(scope).state == InstallState.OUTDATED
    provider.repair(scope)
    assert provider.status(scope).state == InstallState.CURRENT
