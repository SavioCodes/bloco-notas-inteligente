from .config import get_database_path
from .db import NotesRepository
from .ui import SmartNotepadApp


def main() -> None:
    repository = NotesRepository(get_database_path())
    app = SmartNotepadApp(repository)
    app.run()

