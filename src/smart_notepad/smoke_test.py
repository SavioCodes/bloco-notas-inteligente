from __future__ import annotations

import tempfile
import tkinter as tk
import sqlite3
from pathlib import Path

from .backup import BackupManager
from .db import NotesRepository
from .settings import SettingsStore
from .ui import SmartNotepadApp
from . import ui as ui_module


def run_user_flow_smoke_test() -> Path:
    """Exercise the main user flow without requiring manual clicks."""
    with tempfile.TemporaryDirectory() as temp_root:
        base_dir = Path(temp_root)
        export_path = base_dir / "nota-exportada.md"

        original_askyesno = ui_module.messagebox.askyesno
        original_saveas = ui_module.filedialog.asksaveasfilename

        try:
            ui_module.messagebox.askyesno = lambda *_args, **_kwargs: True
            ui_module.filedialog.asksaveasfilename = lambda *_args, **_kwargs: str(export_path)

            database_path = base_dir / "notes.sqlite3"
            repository = NotesRepository(database_path)
            settings_store = SettingsStore(base_dir / "settings.json")
            backup_manager = BackupManager(database_path, base_dir / "backups", retention=5)
            app = SmartNotepadApp(repository, settings_store=settings_store, backup_manager=backup_manager)
            app.root.withdraw()

            try:
                app.root.update_idletasks()
                app.root.update()

                _write_note(app)
                note_id = app.current_note_id
                if note_id is None:
                    raise AssertionError("Nenhuma nota ativa foi criada.")

                _assert_search_finds_note(app, note_id)
                _assert_preview(app)
                _assert_theme_switch(app)
                _assert_trash_and_restore(app, repository, note_id)
                _assert_export(app, export_path)
                _assert_backup(app, backup_manager)
                _assert_encryption(app, repository, note_id)
            finally:
                app.root.destroy()

            return export_path
        finally:
            ui_module.messagebox.askyesno = original_askyesno
            ui_module.filedialog.asksaveasfilename = original_saveas


def _write_note(app: SmartNotepadApp) -> None:
    app.title_var.set("Nota de teste do usuario")
    app.tags_var.set("teste, fluxo")
    app.editor.configure(state=tk.NORMAL)
    app.editor.delete("1.0", tk.END)
    app.editor.insert(
        "1.0",
        "Fluxo de usuario\n\n"
        "## Checklist\n\n"
        "- [ ] testar lixeira\n"
        "- [ ] restaurar nota\n\n"
        "> Preview Markdown tambem deve renderizar citacao.\n\n"
        "Esta nota valida busca, lixeira, restauracao e exportacao Markdown.",
    )
    app._save_current_note()

    saved = app.repository.get_note(app.current_note_id)
    if saved.title != "Nota de teste do usuario":
        raise AssertionError("A nota nao foi salva com o titulo esperado.")
    if "lixeira" not in saved.content:
        raise AssertionError("A nota nao foi salva com o conteudo esperado.")


def _assert_search_finds_note(app: SmartNotepadApp, note_id: int) -> None:
    app.search_var.set("restauracao")
    app._load_notes(note_id)
    if note_id not in app.note_ids:
        raise AssertionError("A busca nao encontrou a nota criada.")
    app.search_var.set("")
    app._load_notes(note_id)


def _assert_preview(app: SmartNotepadApp) -> None:
    app._refresh_preview()
    preview = app.preview.get("1.0", tk.END)
    if "Checklist" not in preview or "Preview Markdown" not in preview:
        raise AssertionError("A preview Markdown nao renderizou o conteudo esperado.")


def _assert_theme_switch(app: SmartNotepadApp) -> None:
    for theme in ("dark", "light", "paper"):
        app._change_theme(theme)
    if app.settings.theme_name != "paper":
        raise AssertionError("A troca de tema nao foi persistida corretamente.")


def _assert_trash_and_restore(app: SmartNotepadApp, repository: NotesRepository, note_id: int) -> None:
    app._move_current_note_to_trash()
    trashed = repository.list_notes(only_deleted=True)
    if note_id not in [note.id for note in trashed]:
        raise AssertionError("A nota nao foi movida para a lixeira.")

    app._set_view_mode("trash", select_id=note_id)
    app._restore_current_note()
    restored = repository.get_note(note_id)
    if restored.deleted_at is not None:
        raise AssertionError("A nota nao foi restaurada corretamente.")


def _assert_export(app: SmartNotepadApp, export_path: Path) -> None:
    app._export_markdown()
    if not export_path.exists():
        raise AssertionError("A exportacao Markdown nao criou arquivo.")

    exported = export_path.read_text(encoding="utf-8")
    if "# Nota de teste do usuario" not in exported:
        raise AssertionError("O Markdown exportado nao contem o titulo esperado.")
    if "restauracao" not in exported:
        raise AssertionError("O Markdown exportado nao contem o conteudo esperado.")


def _assert_backup(app: SmartNotepadApp, backup_manager: BackupManager) -> None:
    app._create_backup_now("smoke")
    if not backup_manager.list_backups():
        raise AssertionError("O backup automatico/manual nao criou copia do banco.")


def _assert_encryption(app: SmartNotepadApp, repository: NotesRepository, note_id: int) -> None:
    password = "SenhaTeste123!"
    app._enable_encryption(password)
    if not app.settings.encryption_enabled:
        raise AssertionError("A protecao por senha nao foi ativada.")
    connection = sqlite3.connect(repository.database_path)
    try:
        raw_content = connection.execute("SELECT content FROM notes WHERE id = ?", (note_id,)).fetchone()[0]
    finally:
        connection.close()
    if not str(raw_content).startswith("sni1:"):
        raise AssertionError("O conteudo da nota nao foi criptografado no SQLite.")
    encrypted_results = repository.list_notes("restauracao")
    if note_id not in [note.id for note in encrypted_results]:
        raise AssertionError("A busca nao funcionou com notas criptografadas desbloqueadas.")

    app._disable_encryption(password)
    if app.settings.encryption_enabled:
        raise AssertionError("A protecao por senha nao foi desativada.")
