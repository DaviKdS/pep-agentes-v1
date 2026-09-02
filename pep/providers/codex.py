"""Codex provider adapter."""

from __future__ import annotations

import filecmp
import re
import shutil
from pathlib import Path

from pep.core import paths
from pep.core.markers import block_state, read_managed_block, remove_block, upsert_block
from pep.core.models import InstallState, OperationResult, Scope, Status

START = "<!-- PEP-CODEX:START"
END = "<!-- PEP-CODEX:END -->"
BLOCK_RE = re.compile(r"<!-- PEP-CODEX:START.*?<!-- PEP-CODEX:END -->", re.DOTALL)
HEADER = (
    "# Instrucoes do projeto (Codex)\n\n"
    "Bloco PEP-Codex gerenciado por scripts/install_codex.py.\n\n"
)


class CodexProvider:
    name = "codex"
    display_name = "Codex"

    @property
    def source_agents(self) -> Path:
        return paths.package_root() / "codex" / "AGENTS.md"

    @property
    def source_skill(self) -> Path:
        return paths.package_root() / "codex" / "skills" / "pepcodex"

    @property
    def source_prompt(self) -> Path:
        return paths.package_root() / "codex" / "prompts" / "pepcodex.md"

    def prompt_path(self) -> Path:
        return self.source_prompt

    def block(self) -> str:
        return read_managed_block(self.source_agents, BLOCK_RE)

    def targets_for(self, scope: Scope) -> tuple[Path, Path]:
        if scope.is_global:
            return scope.path / "AGENTS.md", paths.user_home() / ".agents" / "skills" / "pepcodex"
        return scope.path / "AGENTS.md", scope.path / ".agents" / "skills" / "pepcodex"

    def legacy_prompt_target(self) -> Path:
        return paths.user_home() / ".codex" / "prompts" / "pepcodex.md"

    def _copy_skill(self, dest: Path, force: bool) -> str:
        if dest.exists():
            if not force:
                return "ja existe (use --force para atualizar)"
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(self.source_skill, dest)
        return "instalada"

    def _skill_matches(self, dest: Path) -> bool:
        if not dest.exists():
            return False
        src_files = sorted(p.relative_to(self.source_skill) for p in self.source_skill.rglob("*") if p.is_file())
        dst_files = sorted(p.relative_to(dest) for p in dest.rglob("*") if p.is_file())
        if src_files != dst_files:
            return False
        return all(filecmp.cmp(self.source_skill / rel, dest / rel, shallow=False) for rel in src_files)

    def install(self, scope: Scope, force: bool = False, legacy_prompt: bool = False) -> OperationResult:
        agents, skill = self.targets_for(scope)
        messages = [f"AGENTS.md: {upsert_block(agents, self.block(), BLOCK_RE, START, END, HEADER)} -> {agents}"]
        messages.append(f"$pepcodex: {self._copy_skill(skill, force)} -> {skill}")
        if legacy_prompt:
            dest = self.legacy_prompt_target()
            if dest.exists() and not force:
                messages.append(f"/prompts:pepcodex: ja existe (use --force para atualizar) -> {dest}")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(self.source_prompt, dest)
                messages.append(f"/prompts:pepcodex: instalado -> {dest}")
        return OperationResult(self.name, scope, tuple(messages))

    def uninstall(self, scope: Scope, legacy_prompt: bool = False) -> OperationResult:
        agents, skill = self.targets_for(scope)
        messages = [f"AGENTS.md: {remove_block(agents, BLOCK_RE, START, END)} -> {agents}"]
        if skill.exists():
            shutil.rmtree(skill)
            messages.append(f"$pepcodex: removida -> {skill}")
        else:
            messages.append(f"$pepcodex: inexistente -> {skill}")
        if legacy_prompt:
            dest = self.legacy_prompt_target()
            if dest.exists():
                dest.unlink()
                messages.append(f"/prompts:pepcodex: removido -> {dest}")
            else:
                messages.append(f"/prompts:pepcodex: inexistente -> {dest}")
        return OperationResult(self.name, scope, tuple(messages))

    def status(self, scope: Scope, legacy_prompt: bool = False) -> Status:
        agents, skill = self.targets_for(scope)
        md_state = block_state(agents, self.block(), BLOCK_RE, START, END)
        skill_ok = self._skill_matches(skill)
        legacy_ok = True
        if legacy_prompt:
            dest = self.legacy_prompt_target()
            legacy_ok = dest.exists() and filecmp.cmp(self.source_prompt, dest, shallow=False)
        if md_state == "corrupt":
            state = InstallState.CORRUPT
        elif md_state == "missing" and not skill.exists():
            state = InstallState.NOT_INSTALLED
        elif md_state == "current" and skill_ok and legacy_ok:
            state = InstallState.CURRENT
        elif md_state == "outdated" or (skill.exists() and not skill_ok) or not legacy_ok:
            state = InstallState.OUTDATED
        else:
            state = InstallState.PARTIAL
        detail = f"AGENTS.md={md_state}; skill={'ok' if skill_ok else 'missing/outdated'}"
        if legacy_prompt:
            detail += f"; legacy={'ok' if legacy_ok else 'missing/outdated'}"
        return Status(self.name, scope, state, detail)

    def repair(self, scope: Scope, legacy_prompt: bool = False) -> OperationResult:
        status = self.status(scope, legacy_prompt)
        if status.state == InstallState.CURRENT:
            return OperationResult(self.name, scope, ("Codex ja esta atualizado.",))
        if status.state == InstallState.CORRUPT:
            return OperationResult(self.name, scope, ("Markers corrompidos; reparo automatico cancelado para preservar conteudo manual.",))
        return self.install(scope, force=True, legacy_prompt=legacy_prompt)
