import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .models import Note, utc_now_iso
from .security import decrypt_text, encrypt_text, is_encrypted


class NotesRepository:
    def __init__(self, database_path: Path, password: str | None = None) -> None:
        self.database_path = Path(database_path)
        self.password = password
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._setup()

    def set_password(self, password: str | None) -> None:
        self.password = password

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _setup(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL DEFAULT '',
                    tags TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    deleted_at TEXT
                )
                """
            )
            self._ensure_column(connection, "notes", "deleted_at", "TEXT")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_notes_updated_at ON notes(updated_at)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_notes_title ON notes(title)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_notes_deleted_at ON notes(deleted_at)")

    @staticmethod
    def _ensure_column(connection: sqlite3.Connection, table_name: str, column_name: str, column_type: str) -> None:
        columns = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        if column_name not in {str(column["name"]) for column in columns}:
            connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

    def create_note(self, title: str = "Nota sem titulo", content: str = "", tags: list[str] | None = None) -> Note:
        now = utc_now_iso()
        stored_title, stored_content, stored_tags = self._prepare_for_storage(title.strip() or "Nota sem titulo", content, tags or [])
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO notes (title, content, tags, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (stored_title, stored_content, stored_tags, now, now),
            )
            note_id = int(cursor.lastrowid)
        return self.get_note(note_id)

    def get_note(self, note_id: int) -> Note:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
        if row is None:
            raise KeyError(f"Note {note_id} was not found.")
        return self._row_to_note(row)

    def list_notes(self, query: str = "", *, include_deleted: bool = False, only_deleted: bool = False) -> list[Note]:
        search = query.strip()
        conditions: list[str] = []
        parameters: list[str] = []

        if only_deleted:
            conditions.append("deleted_at IS NOT NULL")
        elif not include_deleted:
            conditions.append("deleted_at IS NULL")

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        with self._connect() as connection:
            rows = connection.execute(
                f"SELECT * FROM notes {where_clause} ORDER BY updated_at DESC, id DESC",
                parameters,
            ).fetchall()
        notes = [self._row_to_note(row) for row in rows]
        if search:
            needle = search.casefold()
            notes = [
                note
                for note in notes
                if needle in note.title.casefold()
                or needle in note.content.casefold()
                or any(needle in tag.casefold() for tag in note.tags)
            ]
        return notes

    def update_note(self, note_id: int, title: str, content: str, tags: list[str]) -> Note:
        stored_title, stored_content, stored_tags = self._prepare_for_storage(title.strip() or "Nota sem titulo", content, tags)
        now = utc_now_iso()
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE notes
                SET title = ?, content = ?, tags = ?, updated_at = ?
                WHERE id = ?
                """,
                (stored_title, stored_content, stored_tags, now, note_id),
            )
        return self.get_note(note_id)

    def delete_note(self, note_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    def move_to_trash(self, note_id: int) -> None:
        now = utc_now_iso()
        with self._connect() as connection:
            connection.execute(
                "UPDATE notes SET deleted_at = ?, updated_at = ? WHERE id = ?",
                (now, now, note_id),
            )

    def restore_note(self, note_id: int) -> Note:
        now = utc_now_iso()
        with self._connect() as connection:
            connection.execute(
                "UPDATE notes SET deleted_at = NULL, updated_at = ? WHERE id = ?",
                (now, note_id),
            )
        return self.get_note(note_id)

    def delete_note_forever(self, note_id: int) -> None:
        self.delete_note(note_id)

    def empty_trash(self) -> int:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM notes WHERE deleted_at IS NOT NULL")
            return int(cursor.rowcount)

    def encrypt_all_notes(self, password: str) -> None:
        previous_password = self.password
        self.password = password
        try:
            notes = self.list_notes(include_deleted=True)
            with self._connect() as connection:
                for note in notes:
                    stored_title, stored_content, stored_tags = self._prepare_for_storage(note.title, note.content, note.tags)
                    connection.execute(
                        "UPDATE notes SET title = ?, content = ?, tags = ? WHERE id = ?",
                        (stored_title, stored_content, stored_tags, note.id),
                    )
        except Exception:
            self.password = previous_password
            raise

    def decrypt_all_notes(self, password: str) -> None:
        previous_password = self.password
        self.password = password
        try:
            notes = self.list_notes(include_deleted=True)
            with self._connect() as connection:
                for note in notes:
                    connection.execute(
                        "UPDATE notes SET title = ?, content = ?, tags = ? WHERE id = ?",
                        (note.title, note.content, json.dumps(self._normalize_tags(note.tags)), note.id),
                    )
        finally:
            self.password = previous_password

    def _prepare_for_storage(self, title: str, content: str, tags: list[str]) -> tuple[str, str, str]:
        normalized_tags = self._normalize_tags(tags)
        serialized_tags = json.dumps(normalized_tags)
        if not self.password:
            return title, content, serialized_tags
        return (
            encrypt_text(title, self.password),
            encrypt_text(content, self.password),
            encrypt_text(serialized_tags, self.password),
        )

    def _decode_text(self, value: str, fallback: str = "") -> str:
        if not is_encrypted(value):
            return value
        if not self.password:
            return fallback
        return decrypt_text(value, self.password)

    def _decode_tags(self, value: str) -> list[str]:
        decoded = self._decode_text(value, "[]")
        try:
            tags = json.loads(decoded)
        except json.JSONDecodeError:
            tags = []
        return list(tags)

    @staticmethod
    def _normalize_tags(tags: list[str]) -> list[str]:
        seen: set[str] = set()
        normalized: list[str] = []
        for tag in tags:
            clean = tag.strip().lower().replace(" ", "-")
            if clean and clean not in seen:
                seen.add(clean)
                normalized.append(clean)
        return normalized

    def _row_to_note(self, row: sqlite3.Row) -> Note:
        title = self._decode_text(str(row["title"]), "Nota protegida")
        content = self._decode_text(str(row["content"]), "")
        tags = self._decode_tags(str(row["tags"]))
        return Note(
            id=int(row["id"]),
            title=title,
            content=content,
            tags=tags,
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
            deleted_at=str(row["deleted_at"]) if row["deleted_at"] is not None else None,
        )
