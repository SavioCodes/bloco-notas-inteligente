import sqlite3
import tempfile
import unittest
from pathlib import Path

from smart_notepad.db import NotesRepository


class NotesRepositoryTests(unittest.TestCase):
    def test_creates_updates_and_searches_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = NotesRepository(Path(temp_dir) / "notes.sqlite3")

            note = repository.create_note("Ideias", "Plano do projeto", ["Projeto", "ideias"])
            updated = repository.update_note(note.id, "Ideias novas", "Conteudo revisado", ["projeto"])
            results = repository.list_notes("revisado")

            self.assertEqual(updated.title, "Ideias novas")
            self.assertEqual(updated.tags, ["projeto"])
            self.assertEqual([result.id for result in results], [note.id])

    def test_delete_note_removes_it_from_list(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = NotesRepository(Path(temp_dir) / "notes.sqlite3")

            note = repository.create_note("Temporaria")
            repository.delete_note(note.id)

            self.assertEqual(repository.list_notes(), [])

    def test_move_to_trash_and_restore_note(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = NotesRepository(Path(temp_dir) / "notes.sqlite3")

            note = repository.create_note("Recuperavel")
            repository.move_to_trash(note.id)

            self.assertEqual(repository.list_notes(), [])
            trashed = repository.list_notes(only_deleted=True)
            self.assertEqual([item.id for item in trashed], [note.id])
            self.assertIsNotNone(trashed[0].deleted_at)

            restored = repository.restore_note(note.id)

            self.assertIsNone(restored.deleted_at)
            self.assertEqual([item.id for item in repository.list_notes()], [note.id])
            self.assertEqual(repository.list_notes(only_deleted=True), [])

    def test_empty_trash_removes_only_deleted_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = NotesRepository(Path(temp_dir) / "notes.sqlite3")

            active = repository.create_note("Ativa")
            deleted = repository.create_note("Na lixeira")
            repository.move_to_trash(deleted.id)

            removed = repository.empty_trash()

            self.assertEqual(removed, 1)
            self.assertEqual([item.id for item in repository.list_notes()], [active.id])
            self.assertEqual(repository.list_notes(only_deleted=True), [])

    def test_migrates_database_without_deleted_at_column(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "old.sqlite3"
            connection = sqlite3.connect(database_path)
            try:
                connection.execute(
                    """
                    CREATE TABLE notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL DEFAULT '',
                        tags TEXT NOT NULL DEFAULT '[]',
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                    """
                )
                connection.commit()
            finally:
                connection.close()

            repository = NotesRepository(database_path)
            note = repository.create_note("Migrada")
            repository.move_to_trash(note.id)

            self.assertEqual(repository.list_notes(), [])
            self.assertEqual([item.id for item in repository.list_notes(only_deleted=True)], [note.id])

    def test_encrypts_and_decrypts_all_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "notes.sqlite3"
            repository = NotesRepository(database_path)
            note = repository.create_note("Privada", "Conteudo secreto", ["segredo"])

            repository.encrypt_all_notes("senha-forte")
            repository.set_password("senha-forte")
            encrypted_note = repository.get_note(note.id)

            self.assertEqual(encrypted_note.title, "Privada")
            self.assertEqual(encrypted_note.content, "Conteudo secreto")
            self.assertEqual(encrypted_note.tags, ["segredo"])
            self.assertEqual([item.id for item in repository.list_notes("secreto")], [note.id])

            connection = sqlite3.connect(database_path)
            try:
                raw = connection.execute("SELECT title, content, tags FROM notes WHERE id = ?", (note.id,)).fetchone()
            finally:
                connection.close()
            self.assertTrue(str(raw[0]).startswith("sni1:"))
            self.assertTrue(str(raw[1]).startswith("sni1:"))
            self.assertTrue(str(raw[2]).startswith("sni1:"))

            repository.decrypt_all_notes("senha-forte")
            repository.set_password(None)
            decrypted = repository.get_note(note.id)

            self.assertEqual(decrypted.title, "Privada")
            self.assertEqual(decrypted.content, "Conteudo secreto")


if __name__ == "__main__":
    unittest.main()
