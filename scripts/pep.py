#!/usr/bin/env python3
"""CLI administrativa central do PEP-Agentes Manager."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pep.core.version import __version__  # noqa: E402
from pep.services.manager import (  # noqa: E402
    collect_doctor,
    collect_status,
    format_results,
    format_status,
    resolve_scopes,
    run_operation,
)

PROVIDERS = ("claude", "codex", "all")


def add_scope_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--here", action="store_true", help="usar o diretorio atual")
    parser.add_argument("--path", action="append", metavar="CAMINHO", help="usar um projeto especifico")
    parser.add_argument("--global", dest="global_scope", action="store_true", help="usar instalacao global")
    parser.add_argument("--legacy-prompt", action="store_true", help="incluir /prompts:pepcodex para Codex")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PEP-Agentes Manager")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("install", "update", "uninstall", "repair", "status"):
        p = sub.add_parser(command)
        p.add_argument("provider", nargs="?", default="all", choices=PROVIDERS)
        add_scope_args(p)
        if command in {"install", "update"}:
            p.add_argument("--force", action="store_true", help="sobrescrever arquivos gerenciados")
    p = sub.add_parser("doctor")
    p.add_argument("provider", nargs="?", default="all", choices=PROVIDERS)
    add_scope_args(p)
    sub.add_parser("version")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "version":
        print(__version__)
        return 0

    scopes = resolve_scopes(args.here, args.path, args.global_scope)
    if not scopes:
        print("Nenhum alvo selecionado. Use --here, --path CAMINHO ou --global.")
        return 2

    if args.command == "status":
        print(format_status(collect_status(args.provider, scopes, args.legacy_prompt)))
        return 0
    if args.command == "doctor":
        print(collect_doctor(args.provider, scopes, args.legacy_prompt))
        return 0

    results = run_operation(
        args.command,
        args.provider,
        scopes,
        force=getattr(args, "force", False),
        legacy_prompt=args.legacy_prompt,
    )
    print(format_results(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
