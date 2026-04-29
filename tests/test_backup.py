import sqlite3
import tempfile
import unittest
from pathlib import Path

from smart_notepad.backup import BackupManager
from smart_notepad.db import NotesRepository


class BackupManagerTests(unittest.TestCase):
    def test_creates_sqlite_backup_and_prunes_old_copies(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            database_path = root / "notes.sqlite3"
            repository = NotesRepository(database_path)
            repository.create_note("Backup", "Conteudo")
            manager = BackupManager(database_path, root / "backups", retention=1)

            first = manager.create_backup("teste")
            second = manager.create_backup("teste")

            self.assertIsNotNone(first)
            self.assertIsNotNone(second)
            backups = manager.list_backups()
            self.assertEqual(len(backups), 1)

            connection = sqlite3.connect(backups[0])
            try:
                count = connection.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()

