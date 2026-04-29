import os
import sys
from pathlib import Path


APP_DIR_NAME = "BlocoNotasInteligente"
LINUX_APP_DIR_NAME = "bloco-notas-inteligente"
DATABASE_NAME = "notes.sqlite3"
SETTINGS_NAME = "settings.json"


def get_data_dir() -> Path:
    """Return the cross-platform writable data directory for the app."""
    override = os.environ.get("SMART_NOTEPAD_HOME")
    if override:
        data_dir = Path(override).expanduser()
    elif sys.platform.startswith("win"):
        base = os.environ.get("LOCALAPPDATA")
        data_dir = Path(base) / APP_DIR_NAME if base else Path.home() / "AppData" / "Local" / APP_DIR_NAME
    else:
        base = os.environ.get("XDG_DATA_HOME")
        data_dir = Path(base) / LINUX_APP_DIR_NAME if base else Path.home() / ".local" / "share" / LINUX_APP_DIR_NAME

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_database_path() -> Path:
    return get_data_dir() / DATABASE_NAME


def get_settings_path() -> Path:
    return get_data_dir() / SETTINGS_NAME


def get_backup_dir() -> Path:
    backup_dir = get_data_dir() / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir
