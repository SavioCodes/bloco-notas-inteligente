import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .models import Note, utc_now_iso


class NotesRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._setup()

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
        normalized_tags = self._normalize_tags(tags or [])
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO notes (title, content, tags, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title.strip() or "Nota sem titulo", content, json.dumps(normalized_tags), now, now),
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

        if search:
            like = f"%{search}%"
            conditions.append("(title LIKE ? OR content LIKE ? OR tags LIKE ?)")
            parameters.extend([like, like, like])

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        with self._connect() as connection:
            rows = connection.execute(
                f"SELECT * FROM notes {where_clause} ORDER BY updated_at DESC, id DESC",
                parameters,
            ).fetchall()
        return [self._row_to_note(row) for row in rows]

    def update_note(self, note_id: int, title: str, content: str, tags: list[str]) -> Note:
        normalized_tags = self._normalize_tags(tags)
        now = utc_now_iso()
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE notes
                SET title = ?, content = ?, tags = ?, updated_at = ?
                WHERE id = ?
                """,
                (title.strip() or "Nota sem titulo", content, json.dumps(normalized_tags), now, note_id),
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

    @staticmethod
    def _row_to_note(row: sqlite3.Row) -> Note:
        try:
            tags = json.loads(row["tags"])
        except json.JSONDecodeError:
            tags = []
        return Note(
            id=int(row["id"]),
            title=str(row["title"]),
            content=str(row["content"]),
            tags=list(tags),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
            deleted_at=str(row["deleted_at"]) if row["deleted_at"] is not None else None,
        )
