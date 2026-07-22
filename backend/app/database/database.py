from __future__ import annotations

import sqlite3
from pathlib import Path

DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[3] / "database" / "football_collection.db"


class Database:
    def __init__(self, path: str | Path = DEFAULT_DATABASE_PATH):
        self.path = Path(path)

    def exists(self) -> bool:
        return self.path.exists()

    def connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection