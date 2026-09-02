"""Claude Code provider adapter."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from pep.core import paths
from pep.core.markers import block_state, read_managed_block, remove_block, upsert_block
from pep.core.models import InstallState, OperationResult, Scope, Status

START = "<!-- PEP-AGENTES:START"
END = "<!-- PEP-AGENTES:END -->"
BLOCK_RE = re.compile(r"<!-- PEP-AGENTES:START.*?<!-- PEP-AGENTES:END -->", re.DOTALL)
HEADER = (
    "# Instrucoes do projeto (Claude Code)\n\n"
    "Bloco PEP-Agentes gerenciado por scripts/install_claude.py (nao edite entre os marcadores).\n\n"
)


class ClaudeProvider:
    name = "claude"
    display_name = "Claude Code"

    @property
    def source_claude_md(self) -> Path:
        return paths.package_root() / "claude" / "CLAUDE.md"

    @property
    def source_command(self) -> Path:
        return paths.package_root() / "claude" / "commands" / "pep.md"

    def prompt_path(self) -> Path:
        return paths.package_root() / "prompts" / "pep-agentes-claude.txt"

    def block(self) -> str:
        return read_managed_block(self.source_claude_md, BLOCK_RE)

    def command_text(self) -> str:
        return self.source_command.read_text(encoding="utf-8")

    def targets_for(self, scope: Scope) -> tuple[Path, Path]:
        if scope.is_global:
            base = scope.path
            return base / "CLAUDE.md", base / "commands" / "pep.md"
        return scope.path / "CLAUDE.md", scope.path / ".claude" / "commands" / "pep.md"

    def install(self, scope: Scope, force: bool = False, legacy_prompt: bool = False) -> OperationResult:
        del legacy_prompt
        claude_md, command_path = self.targets_for(scope)
        block = self.block()
        command_text = self.command_text()
        messages = [f"CLAUDE.md: {upsert_block(claude_md, block, BLOCK_RE, START, END, HEADER)} -> {claude_md}"]
        command_path.parent.mkdir(parents=True, exist_ok=True)
        if command_path.exists() and not force:
            if command_path.read_text(encoding="utf-8") == command_text:
                messages.append(f"/pep: ja atualizado -> {command_path}")
            else:
                messages.append(f"/pep: JA EXISTE (use --force para sobrescrever) -> {command_path}")
        else:
            command_path.write_text(command_text, encoding="utf-8")
            messages.append(f"/pep: instalado -> {command_path}")
        return OperationResult(self.name, scope, tuple(messages))

    def uninstall(self, scope: Scope, legacy_prompt: bool = False) -> OperationResult:
        del legacy_prompt
        claude_md, command_path = self.targets_for(scope)
        messages = [f"CLAUDE.md: {remove_block(claude_md, BLOCK_RE, START, END)} -> {claude_md}"]
        if command_path.exists():
            command_path.unlink()
            messages.append(f"/pep: removido -> {command_path}")
        else:
            messages.append(f"/pep: inexistente -> {command_path}")
        return OperationResult(self.name, scope, tuple(messages))

    def status(self, scope: Scope, legacy_prompt: bool = False) -> Status:
        del legacy_prompt
        claude_md, command_path = self.targets_for(scope)
        block = self.block()
        md_state = block_state(claude_md, block, BLOCK_RE, START, END)
        command_ok = command_path.exists() and command_path.read_text(encoding="utf-8") == self.command_text()
        if md_state == "corrupt":
            state = InstallState.CORRUPT
        elif md_state == "missing" and not command_path.exists():
            state = InstallState.NOT_INSTALLED
        elif md_state == "current" and command_ok:
            state = InstallState.CURRENT
        elif md_state == "outdated" or (command_path.exists() and not command_ok):
            state = InstallState.OUTDATED
        else:
            state = InstallState.PARTIAL
        return Status(self.name, scope, state, f"CLAUDE.md={md_state}; command={'ok' if command_ok else 'missing/outdated'}")

    def repair(self, scope: Scope, legacy_prompt: bool = False) -> OperationResult:
        status = self.status(scope, legacy_prompt)
        if status.state == InstallState.CURRENT:
            return OperationResult(self.name, scope, ("Claude Code ja esta atualizado.",))
        if status.state == InstallState.CORRUPT:
            return OperationResult(self.name, scope, ("Markers corrompidos; reparo automatico cancelado para preservar conteudo manual.",))
        return self.install(scope, force=True)
