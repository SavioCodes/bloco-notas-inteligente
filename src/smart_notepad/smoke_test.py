from __future__ import annotations

import tempfile
import tkinter as tk
from pathlib import Path

from .db import NotesRepository
from .ui import SmartNotepadApp
from . import ui as ui_module


def run_user_flow_smoke_test() -> Path:
    """Exercise the main user flow without requiring manual clicks."""
    temp_root = tempfile.TemporaryDirectory()
    base_dir = Path(temp_root.name)
    export_path = base_dir / "nota-exportada.md"

    original_askyesno = ui_module.messagebox.askyesno
    original_saveas = ui_module.filedialog.asksaveasfilename

    try:
        ui_module.messagebox.askyesno = lambda *_args, **_kwargs: True
        ui_module.filedialog.asksaveasfilename = lambda *_args, **_kwargs: str(export_path)

        repository = NotesRepository(base_dir / "notes.sqlite3")
        app = SmartNotepadApp(repository)
        app.root.withdraw()

        try:
            app.root.update_idletasks()
            app.root.update()

            _write_note(app)
            note_id = app.current_note_id
            if note_id is None:
                raise AssertionError("Nenhuma nota ativa foi criada.")

            _assert_search_finds_note(app, note_id)
            _assert_trash_and_restore(app, repository, note_id)
            _assert_export(app, export_path)
        finally:
            app.root.destroy()

        return export_path
    except Exception:
        temp_root.cleanup()
        raise
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
        "- [ ] testar lixeira\n"
        "- [ ] restaurar nota\n\n"
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
