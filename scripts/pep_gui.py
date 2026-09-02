#!/usr/bin/env python3
"""Interface grafica unificada do PEP-Agentes Manager."""

from __future__ import annotations

import io
import sys
import threading
from contextlib import redirect_stdout
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pep.core.models import Scope  # noqa: E402
from pep.core.version import APP_TITLE  # noqa: E402
from pep.providers import get_provider  # noqa: E402
from pep.services.manager import (  # noqa: E402
    collect_doctor,
    collect_status,
    format_results,
    format_status,
    run_operation,
)

PROVIDER_LABELS = {
    "Claude": "claude",
    "Codex": "codex",
    "Todos": "all",
}
ACTION_LABELS = {
    "Instalar": "install",
    "Atualizar": "update",
    "Reparar": "repair",
    "Desinstalar": "uninstall",
    "Verificar": "status",
}


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PEP-Agentes Manager")
        self.geometry("760x700")
        self.minsize(680, 620)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(self, text=APP_TITLE, font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(18, 0), sticky="w"
        )
        ctk.CTkLabel(
            self,
            text="Manager local para instalar e verificar o protocolo PEP em Claude Code e Codex.",
            text_color=("gray40", "gray70"),
        ).grid(row=1, column=0, padx=20, pady=(0, 12), sticky="w")

        self.provider = self._segmented("Plataforma", ["Claude", "Codex", "Todos"], "Todos", 2)
        self.action = self._segmented(
            "Ação", ["Instalar", "Atualizar", "Reparar", "Desinstalar", "Verificar"], "Instalar", 3
        )
        self.scope_mode = self._segmented(
            "Escopo", ["Projeto atual", "Selecionar pasta", "Múltiplas pastas", "Global"], "Projeto atual", 4
        )

        folders_frame = ctk.CTkFrame(self)
        folders_frame.grid(row=5, column=0, padx=20, pady=6, sticky="ew")
        folders_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(folders_frame, text="Pastas selecionadas").grid(row=0, column=0, padx=12, pady=(10, 4), sticky="w")
        ctk.CTkButton(folders_frame, text="Adicionar pasta...", width=150, command=self._add_folder).grid(
            row=0, column=1, padx=(0, 8), pady=(10, 4), sticky="e"
        )
        ctk.CTkButton(folders_frame, text="Limpar", width=70, command=self._clear_folders).grid(
            row=0, column=2, padx=(0, 12), pady=(10, 4), sticky="e"
        )
        self.folders_box = ctk.CTkTextbox(folders_frame, height=80)
        self.folders_box.grid(row=1, column=0, columnspan=3, padx=12, pady=(0, 12), sticky="ew")

        opts = ctk.CTkFrame(self, fg_color="transparent")
        opts.grid(row=6, column=0, padx=20, pady=(0, 6), sticky="ew")
        self.force_var = ctk.BooleanVar(value=False)
        self.legacy_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(opts, text="Forçar atualização de arquivos gerenciados", variable=self.force_var).pack(
            side="left", padx=(0, 18)
        )
        ctk.CTkCheckBox(opts, text="Codex legacy /prompts:pepcodex", variable=self.legacy_var).pack(side="left")

        prompt_row = ctk.CTkFrame(self, fg_color="transparent")
        prompt_row.grid(row=7, column=0, padx=20, pady=4, sticky="ew")
        ctk.CTkButton(prompt_row, text="Copiar prompt Claude", command=lambda: self._copy_prompt("claude")).pack(
            side="left"
        )
        ctk.CTkButton(prompt_row, text="Copiar prompt Codex", command=lambda: self._copy_prompt("codex")).pack(
            side="left", padx=8
        )
        ctk.CTkButton(prompt_row, text="Doctor", command=self._doctor).pack(side="left")
        self.run_btn = ctk.CTkButton(
            prompt_row, text="Executar", width=160, height=38, font=ctk.CTkFont(size=15, weight="bold"), command=self._run
        )
        self.run_btn.pack(side="right")

        self.log = ctk.CTkTextbox(self, height=220)
        self.log.grid(row=8, column=0, padx=20, pady=(6, 16), sticky="nsew")
        self.log.configure(state="disabled")
        self._write_log("Pronto.")

    def _segmented(self, label: str, values: list[str], default: str, row: int) -> ctk.CTkSegmentedButton:
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=0, padx=20, pady=6, sticky="ew")
        ctk.CTkLabel(frame, text=label).pack(anchor="w", padx=12, pady=(10, 2))
        control = ctk.CTkSegmentedButton(frame, values=values)
        control.set(default)
        control.pack(fill="x", padx=12, pady=(0, 12))
        return control

    def _add_folder(self) -> None:
        path = filedialog.askdirectory(title="Selecione a pasta do projeto")
        if path:
            self.folders_box.insert("end", path.replace("/", "\\") + "\n")

    def _clear_folders(self) -> None:
        self.folders_box.delete("1.0", "end")

    def _write_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.insert("1.0", text)
        self.log.configure(state="disabled")

    def _scopes(self) -> list[Scope]:
        mode = self.scope_mode.get()
        if mode == "Projeto atual":
            return [Scope(Path.cwd(), False)]
        if mode == "Global":
            return [Scope(Path.home(), True)]
        raw = [line.strip() for line in self.folders_box.get("1.0", "end").splitlines() if line.strip()]
        if mode == "Selecionar pasta" and len(raw) > 1:
            raw = raw[:1]
        return [Scope(Path(line).expanduser().resolve(), False) for line in raw]

    def _copy_prompt(self, provider_name: str) -> None:
        try:
            prompt = get_provider(provider_name).prompt_path()
            if prompt is None:
                raise RuntimeError("Provider sem prompt copiavel.")
            self.clipboard_clear()
            self.clipboard_append(prompt.read_text(encoding="utf-8"))
            self._write_log(f"Prompt {provider_name} copiado para a area de transferencia.")
        except Exception as exc:  # noqa: BLE001
            self._write_log(f"ERRO ao copiar prompt: {exc}")

    def _doctor(self) -> None:
        scopes = self._scopes()
        if not scopes:
            messagebox.showwarning("PEP-Agentes Manager", "Selecione ao menos uma pasta.")
            return
        provider = PROVIDER_LABELS[self.provider.get()]
        self._write_log(collect_doctor(provider, scopes, self.legacy_var.get()))

    def _run(self) -> None:
        scopes = self._scopes()
        if not scopes:
            messagebox.showwarning("PEP-Agentes Manager", "Selecione ao menos uma pasta.")
            return
        self.run_btn.configure(state="disabled", text="Executando...")
        threading.Thread(target=self._worker, args=(scopes,), daemon=True).start()

    def _worker(self, scopes: list[Scope]) -> None:
        buf = io.StringIO()
        try:
            provider = PROVIDER_LABELS[self.provider.get()]
            action = ACTION_LABELS[self.action.get()]
            with redirect_stdout(buf):
                if action == "status":
                    print(format_status(collect_status(provider, scopes, self.legacy_var.get())))
                else:
                    print(format_results(run_operation(action, provider, scopes, self.force_var.get(), self.legacy_var.get())))
        except Exception as exc:  # noqa: BLE001
            print(f"ERRO: {exc}", file=buf)
        self.after(0, lambda: self._finish(buf.getvalue()))

    def _finish(self, text: str) -> None:
        self._write_log(text)
        self.run_btn.configure(state="normal", text="Executar")


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
