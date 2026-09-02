"""Small data models used by providers and services."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class InstallState(str, Enum):
    NOT_INSTALLED = "not_installed"
    INSTALLED = "installed"
    CURRENT = "current"
    OUTDATED = "outdated"
    PARTIAL = "partial"
    CORRUPT = "corrupt"


@dataclass(frozen=True)
class Scope:
    path: Path
    is_global: bool = False

    @property
    def label(self) -> str:
        return "GLOBAL" if self.is_global else str(self.path)


@dataclass(frozen=True)
class Status:
    provider: str
    scope: Scope
    state: InstallState
    detail: str


@dataclass(frozen=True)
class OperationResult:
    provider: str
    scope: Scope
    messages: tuple[str, ...]
