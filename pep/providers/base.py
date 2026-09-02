"""Provider protocol shared by Claude and Codex adapters."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from pep.core.models import OperationResult, Scope, Status


class Provider(Protocol):
    name: str
    display_name: str

    def prompt_path(self) -> Path | None: ...

    def install(self, scope: Scope, force: bool = False, legacy_prompt: bool = False) -> OperationResult: ...

    def uninstall(self, scope: Scope, legacy_prompt: bool = False) -> OperationResult: ...

    def status(self, scope: Scope, legacy_prompt: bool = False) -> Status: ...

    def repair(self, scope: Scope, legacy_prompt: bool = False) -> OperationResult: ...
