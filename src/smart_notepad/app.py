from __future__ import annotations

import argparse

from . import __version__
from .backup import BackupManager
from .config import get_backup_dir, get_database_path, get_settings_path
from .db import NotesRepository
from .settings import SettingsStore
from .ui import SmartNotepadApp


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="bloco-notas",
        description="Bloco de Notas Inteligente para Windows e Linux.",
    )
    parser.add_argument("--version", action="store_true", help="Mostra a versao do app e sai.")
    parser.add_argument("--smoke-test", action="store_true", help="Executa um teste automatizado do fluxo principal.")
    args = parser.parse_args(argv)

    if args.version:
        print(f"Bloco de Notas Inteligente {__version__}")
        return

    if args.smoke_test:
        from .smoke_test import run_user_flow_smoke_test

        run_user_flow_smoke_test()
        print("Smoke test OK.")
        return

    database_path = get_database_path()
    settings_store = SettingsStore(get_settings_path())
    settings = settings_store.load()
    repository = NotesRepository(database_path)
    backup_manager = BackupManager(database_path, get_backup_dir(), retention=settings.backup_retention)
    app = SmartNotepadApp(repository, settings_store=settings_store, backup_manager=backup_manager)
    app.run()
