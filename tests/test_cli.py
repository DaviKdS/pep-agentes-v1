from __future__ import annotations

import scripts.pep as pep_cli


def test_version_command(capsys):
    assert pep_cli.main(["version"]) == 0
    assert "1.2.0" in capsys.readouterr().out


def test_scope_is_required(capsys):
    assert pep_cli.main(["status", "codex"]) == 2
    assert "Nenhum alvo selecionado" in capsys.readouterr().out


def test_cli_install_status_uninstall_codex_here(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert pep_cli.main(["install", "codex", "--here"]) == 0
    assert "$pepcodex" in capsys.readouterr().out

    assert pep_cli.main(["status", "codex", "--here"]) == 0
    assert "current" in capsys.readouterr().out

    assert pep_cli.main(["uninstall", "codex", "--here"]) == 0
    assert "Concluido" in capsys.readouterr().out
