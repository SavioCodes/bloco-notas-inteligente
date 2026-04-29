from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class BackupManager:
    def __init__(self, database_path: Path, backup_dir: Path, retention: int = 20) -> None:
        self.database_path = Path(database_path)
        self.backup_dir = Path(backup_dir)
        self.retention = max(1, retention)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, reason: str = "auto") -> Path | None:
        if not self.database_path.exists():
            return None
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        safe_reason = "".join(char for char in reason.lower() if char.isalnum() or char in ("-", "_")) or "auto"
        destination = self.backup_dir / f"notes-{timestamp}-{safe_reason}.sqlite3"

        source = sqlite3.connect(self.database_path)
        target = sqlite3.connect(destination)
        try:
            source.backup(target)
            target.commit()
        finally:
            target.close()
            source.close()

        self.prune()
        return destination

    def create_backup_if_due(self, interval_minutes: int, reason: str = "auto") -> Path | None:
        interval_seconds = max(1, interval_minutes) * 60
        latest = self.latest_backup()
        if latest is None:
            return self.create_backup(reason)
        age = datetime.now(timezone.utc).timestamp() - latest.stat().st_mtime
        if age >= interval_seconds:
            return self.create_backup(reason)
        return None

    def list_backups(self) -> list[Path]:
        return sorted(self.backup_dir.glob("notes-*.sqlite3"), key=lambda path: path.stat().st_mtime, reverse=True)

    def latest_backup(self) -> Path | None:
        backups = self.list_backups()
        return backups[0] if backups else None

    def prune(self) -> None:
        for backup in self.list_backups()[self.retention :]:
            backup.unlink(missing_ok=True)
