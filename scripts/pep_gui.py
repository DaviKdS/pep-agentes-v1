#!/usr/bin/env python3
"""Interface grafica (CustomTkinter) para instalar o PEP-Agentes v1.0 no Claude Code.

Sem digitar comandos: escolha a acao (Instalar/Desinstalar), o destino
(pastas de projeto ou Global ~/.claude) e clique em Executar. Tambem permite
copiar o prompt do Claude (chat) para a area de transferencia.

Reaproveita a logica de scripts/install_claude.py.
"""
from __future__ import annotations

import io
import sys
import threading
from contextlib import redirect_stdout
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

# Permite "import install_claude" tanto como script quanto empacotado no .exe.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import install_claude  # noqa: E402

APP_TITLE = "PEP-Agentes v1.0 — Claude Code"
CHAT_PROMPT_REL = Path("prompts") / "pep-agentes-claude.txt"


def chat_prompt_path() -> Path:
    """Caminho do prompt do Claude (chat), rodando como .py ou empacotado."""
    return install_claude.PACKAGE_ROOT / CHAT_PROMPT_REL


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("640x620")
        self.minsize(560, 560)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # Cabecalho
        ctk.CTkLabel(
            self, text="PEP-Agentes v1.0", font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(18, 0), sticky="w")
        ctk.CTkLabel(
            self, text="Instalar o protocolo no Claude Code sem digitar comandos.",
            text_color=("gray40", "gray70"),
        ).grid(row=1, column=0, padx=20, pady=(0, 12), sticky="w")

        # Acao
        action_frame = ctk.CTkFrame(self)
        action_frame.grid(row=2, column=0, padx=20, pady=6, sticky="ew")
        ctk.CTkLabel(action_frame, text="Ação").pack(anchor="w", padx=12, pady=(10, 2))
        self.action = ctk.CTkSegmentedButton(
            action_frame, values=["Instalar", "Desinstalar"], command=self._on_toggle
        )
        self.action.set("Instalar")
        self.action.pack(fill="x", padx=12, pady=(0, 12))

        # Destino
        dest_frame = ctk.CTkFrame(self)
        dest_frame.grid(row=3, column=0, padx=20, pady=6, sticky="ew")
        ctk.CTkLabel(dest_frame, text="Destino").pack(anchor="w", padx=12, pady=(10, 2))
        self.dest = ctk.CTkSegmentedButton(
            dest_frame, values=["Pastas de projeto", "Global (~/.claude)"],
            command=self._on_toggle,
        )
        self.dest.set("Pastas de projeto")
        self.dest.pack(fill="x", padx=12, pady=(0, 12))

        # Pastas
        self.folders_frame = ctk.CTkFrame(self)
        self.folders_frame.grid(row=4, column=0, padx=20, pady=6, sticky="ew")
        header = ctk.CTkFrame(self.folders_frame, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 4))
        ctk.CTkLabel(header, text="Pasta(s) do projeto").pack(side="left")
        ctk.CTkButton(header, text="Limpar", width=70, command=self._clear_folders).pack(side="right")
        ctk.CTkButton(
            header, text="Adicionar pasta...", width=150, command=self._add_folder
        ).pack(side="right", padx=(0, 8))
        self.folders_box = ctk.CTkTextbox(self.folders_frame, height=90)
        self.folders_box.pack(fill="x", padx=12, pady=(0, 12))

        # Opcoes
        self.force_var = ctk.BooleanVar(value=False)
        self.force_chk = ctk.CTkCheckBox(
            self, text="Sobrescrever comando /pep existente", variable=self.force_var
        )
        self.force_chk.grid(row=5, column=0, padx=24, pady=(0, 6), sticky="w")

        # Log
        self.log = ctk.CTkTextbox(self, height=150)
        self.log.grid(row=6, column=0, padx=20, pady=6, sticky="nsew")
        self.log.configure(state="disabled")

        # Acoes finais
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=7, column=0, padx=20, pady=(6, 16), sticky="ew")
        bottom.grid_columnconfigure(0, weight=1)
        ctk.CTkButton(
            bottom, text="Copiar prompt do Claude (chat)", command=self._copy_chat_prompt,
            fg_color="transparent", border_width=1,
        ).grid(row=0, column=0, sticky="w")
        self.run_btn = ctk.CTkButton(
            bottom, text="Executar", width=160, height=40,
            font=ctk.CTkFont(size=15, weight="bold"), command=self._run,
        )
        self.run_btn.grid(row=0, column=1, sticky="e")

        self._on_toggle(None)

    # ---- helpers de UI ----
    def _on_toggle(self, _value) -> None:
        is_global = self.dest.get().startswith("Global")
        state = "disabled" if is_global else "normal"
        for child in self.folders_frame.winfo_children():
            self._set_state_recursive(child, state)
        color = ("gray70", "gray30") if is_global else None
        if color:
            self.folders_frame.configure(fg_color=color)
        else:
            self.folders_frame.configure(fg_color=("gray86", "gray17"))
        # /force so faz sentido ao instalar
        self.force_chk.configure(
            state="normal" if self.action.get() == "Instalar" else "disabled"
        )

    def _set_state_recursive(self, widget, state) -> None:
        try:
            widget.configure(state=state)
        except Exception:
            pass
        for child in getattr(widget, "winfo_children", lambda: [])():
            self._set_state_recursive(child, state)

    def _add_folder(self) -> None:
        path = filedialog.askdirectory(title="Selecione a pasta do projeto")
        if path:
            self.folders_box.insert("end", path.replace("/", "\\") + "\n")

    def _clear_folders(self) -> None:
        self.folders_box.delete("1.0", "end")

    def _folders(self) -> list[Path]:
        raw = self.folders_box.get("1.0", "end").splitlines()
        return [Path(line.strip()).expanduser() for line in raw if line.strip()]

    def _write_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.insert("1.0", text)
        self.log.configure(state="disabled")

    def _copy_chat_prompt(self) -> None:
        try:
            content = chat_prompt_path().read_text(encoding="utf-8")
            self.clipboard_clear()
            self.clipboard_append(content)
            self._write_log(
                "Prompt do Claude (chat) copiado para a area de transferencia.\n"
                "Cole no inicio de uma conversa nova no Claude (claude.ai)."
            )
        except Exception as exc:  # noqa: BLE001
            self._write_log(f"ERRO ao copiar prompt: {exc}")

    # ---- execucao ----
    def _run(self) -> None:
        is_global = self.dest.get().startswith("Global")
        if is_global:
            targets = [(Path.home() / ".claude", True)]
        else:
            folders = self._folders()
            if not folders:
                self._write_log("Adicione ao menos uma pasta de projeto (botao 'Adicionar pasta...').")
                return
            targets = [(p, False) for p in folders]

        self.run_btn.configure(state="disabled", text="Executando...")
        threading.Thread(
            target=self._worker,
            args=(targets, self.action.get() == "Instalar", self.force_var.get()),
            daemon=True,
        ).start()

    def _worker(self, targets, do_install: bool, force: bool) -> None:
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                if do_install:
                    block = install_claude.read_block()
                    command_text = install_claude.SOURCE_COMMAND.read_text(encoding="utf-8")
                for scope_dir, is_global in targets:
                    label = "GLOBAL (~/.claude)" if is_global else str(scope_dir)
                    print(f"== {label} ==")
                    if do_install:
                        install_claude.install_target(scope_dir, block, command_text, is_global, force)
                    else:
                        install_claude.uninstall_target(scope_dir, is_global)
                    print()
                print("Concluido.")
        except Exception as exc:  # noqa: BLE001
            print(f"\nERRO: {exc}")
        text = buf.getvalue()
        self.after(0, lambda: self._finish(text))

    def _finish(self, text: str) -> None:
        self._write_log(text)
        self.run_btn.configure(state="normal", text="Executar")


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
