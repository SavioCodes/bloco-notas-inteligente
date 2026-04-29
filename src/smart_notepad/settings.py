from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class AppSettings:
    theme_name: str = "paper"
    backup_enabled: bool = True
    backup_interval_minutes: int = 15
    backup_retention: int = 20
    encryption_enabled: bool = False
    password_record: dict[str, Any] | None = None
    preview_visible: bool = True


class SettingsStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> AppSettings:
        if not self.path.exists():
            return AppSettings()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return AppSettings()
        return AppSettings(**{**asdict(AppSettings()), **raw})

    def save(self, settings: AppSettings) -> None:
        self.path.write_text(
            json.dumps(asdict(settings), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

