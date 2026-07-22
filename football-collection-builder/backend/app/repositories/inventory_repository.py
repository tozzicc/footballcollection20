from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.database.database import DEFAULT_DATABASE_PATH, Database
from app.database.schema import SCHEMA_SQL, TABLES
from app.models.inventory import (
    Inventory,
    InventoryCategorySummary,
    InventoryExtensionSummary,
    InventoryFolder,
    InventoryItem,
    InventoryMetadata,
    InventoryStatistics,
)


class InventoryRepository:
    def __init__(self, database_path: str | Path = DEFAULT_DATABASE_PATH):
        self.database = Database(database_path)

    @property
    def database_path(self) -> Path:
        return self.database.path

    def create_database(self) -> bool:
        created = not self.database.exists()
        with self.database.connect() as connection:
            connection.executescript(SCHEMA_SQL)
        return created

    def create_schema(self) -> None:
        with self.database.connect() as connection:
            connection.executescript(SCHEMA_SQL)

    def schema_tables(self) -> list[str]:
        with self.database.connect() as connection:
            rows = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        return [row["name"] for row in rows if row["name"] in TABLES]

    def clear_inventory(self, connection: sqlite3.Connection) -> None:
        for table in TABLES:
            connection.execute(f"DELETE FROM {table}")

    def save(self, inventory: Inventory) -> str:
        self.create_database()
        saved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        connection = self.database.connect()
        try:
            connection.execute("BEGIN")
            self.clear_inventory(connection)
            self._insert_metadata(connection, inventory, saved_at)
            self._insert_statistics(connection, inventory.statistics)
            self._insert_extensions(connection, inventory.extensions)
            self._insert_categories(connection, inventory.categories)
            self._insert_folders(connection, inventory.folders)
            self._insert_items(connection, inventory.items)
            connection.commit()
            return saved_at
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _insert_metadata(self, connection: sqlite3.Connection, inventory: Inventory, saved_at: str) -> None:
        metadata = inventory.metadata
        connection.execute(
            "INSERT INTO inventory_metadata VALUES (1, ?, ?, ?, ?, ?)",
            (metadata.generatedAt, metadata.scannerVersion, metadata.workspacePath, metadata.durationMs, saved_at),
        )

    def _insert_statistics(self, connection: sqlite3.Connection, value: InventoryStatistics) -> None:
        connection.execute(
            "INSERT INTO inventory_statistics VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (value.totalFiles, value.totalDirectories, value.totalSize, value.totalImages, value.totalPages, value.totalVideos, value.totalDocuments, value.totalArchives, value.totalData, value.totalOther),
        )

    def _insert_extensions(self, connection: sqlite3.Connection, values: list[InventoryExtensionSummary]) -> None:
        connection.executemany("INSERT INTO inventory_extensions(extension, count) VALUES (?, ?)", [(value.extension, value.count) for value in values])

    def _insert_categories(self, connection: sqlite3.Connection, values: list[InventoryCategorySummary]) -> None:
        connection.executemany("INSERT INTO inventory_categories(category, count) VALUES (?, ?)", [(value.category, value.count) for value in values])

    def _insert_folders(self, connection: sqlite3.Connection, values: list[InventoryFolder]) -> None:
        connection.executemany(
            "INSERT INTO inventory_folders(path, relative_path, name, parent, depth) VALUES (?, ?, ?, ?, ?)",
            [(value.path, value.relativePath, value.name, value.parent, value.depth) for value in values],
        )

    def _insert_items(self, connection: sqlite3.Connection, values: list[InventoryItem]) -> None:
        connection.executemany(
            "INSERT INTO inventory_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(value.id, value.relativePath, value.absolutePath, value.directory, value.filename, value.extension, value.category, value.size, value.createdAt, value.modifiedAt, int(value.isDirectory), int(value.readable)) for value in values],
        )

    def get_statistics(self) -> InventoryStatistics | None:
        self.create_schema()
        with self.database.connect() as connection:
            row = connection.execute("SELECT * FROM inventory_statistics WHERE id = 1").fetchone()
        return None if row is None else InventoryStatistics(
            totalFiles=row["total_files"], totalDirectories=row["total_directories"], totalSize=row["total_size"],
            totalImages=row["total_images"], totalPages=row["total_pages"], totalVideos=row["total_videos"],
            totalDocuments=row["total_documents"], totalArchives=row["total_archives"], totalData=row["total_data"], totalOther=row["total_other"],
        )

    def get_extensions(self) -> list[InventoryExtensionSummary]:
        self.create_schema()
        with self.database.connect() as connection:
            rows = connection.execute("SELECT extension, count FROM inventory_extensions ORDER BY count DESC, extension").fetchall()
        return [InventoryExtensionSummary(extension=row["extension"], count=row["count"]) for row in rows]

    def get_categories(self) -> list[InventoryCategorySummary]:
        self.create_schema()
        with self.database.connect() as connection:
            rows = connection.execute("SELECT category, count FROM inventory_categories ORDER BY category").fetchall()
        return [InventoryCategorySummary(category=row["category"], count=row["count"]) for row in rows]

    def get_first_items(self, limit: int = 50) -> list[InventoryItem]:
        self.create_schema()
        with self.database.connect() as connection:
            rows = connection.execute("SELECT * FROM inventory_items ORDER BY relative_path LIMIT ?", (limit,)).fetchall()
        return [InventoryItem(
            id=row["id"], relativePath=row["relative_path"], absolutePath=row["absolute_path"], directory=row["directory"],
            filename=row["filename"], extension=row["extension"], category=row["category"], size=row["size"],
            createdAt=row["created_at"], modifiedAt=row["modified_at"], isDirectory=bool(row["is_directory"]), readable=bool(row["readable"]),
        ) for row in rows]

    def get_html_pages(self) -> list[InventoryItem]:
        self.create_schema()
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT * FROM inventory_items
                   WHERE category = 'pages' AND lower(extension) IN ('.htm', '.html', '.asp')
                   ORDER BY relative_path"""
            ).fetchall()
        return [InventoryItem(
            id=row["id"], relativePath=row["relative_path"], absolutePath=row["absolute_path"],
            directory=row["directory"], filename=row["filename"], extension=row["extension"],
            category=row["category"], size=row["size"], createdAt=row["created_at"],
            modifiedAt=row["modified_at"], isDirectory=bool(row["is_directory"]),
            readable=bool(row["readable"]),
        ) for row in rows]

    def get_workspace_path(self) -> str | None:
        self.create_schema()
        with self.database.connect() as connection:
            row = connection.execute("SELECT workspace_path FROM inventory_metadata WHERE id = 1").fetchone()
        return None if row is None else row["workspace_path"]

    def get_inventory(self) -> Inventory | None:
        statistics = self.get_statistics()
        if statistics is None:
            return None
        with self.database.connect() as connection:
            metadata_row = connection.execute("SELECT * FROM inventory_metadata WHERE id = 1").fetchone()
            folder_rows = connection.execute("SELECT * FROM inventory_folders ORDER BY id").fetchall()
            item_count = connection.execute("SELECT COUNT(*) AS count FROM inventory_items").fetchone()["count"]
        items = self.get_first_items(item_count)
        return Inventory(
            metadata=InventoryMetadata(generatedAt=metadata_row["generated_at"], scannerVersion=metadata_row["scanner_version"], workspacePath=metadata_row["workspace_path"], durationMs=metadata_row["duration_ms"]),
            statistics=statistics,
            folders=[InventoryFolder(path=row["path"], relativePath=row["relative_path"], name=row["name"], parent=row["parent"], depth=row["depth"]) for row in folder_rows],
            items=items,
            categories=self.get_categories(),
            extensions=self.get_extensions(),
            errors=[],
        )

    def get_status(self) -> dict[str, str | int | bool | None]:
        if not self.database.exists():
            return {"databaseCreated": False, "lastSavedAt": None, "fileCount": 0, "folderCount": 0}
        self.create_schema()
        with self.database.connect() as connection:
            metadata = connection.execute("SELECT saved_at FROM inventory_metadata WHERE id = 1").fetchone()
            files = connection.execute("SELECT COUNT(*) AS count FROM inventory_items").fetchone()["count"]
            folders = connection.execute("SELECT COUNT(*) AS count FROM inventory_folders").fetchone()["count"]
        return {"databaseCreated": True, "lastSavedAt": None if metadata is None else metadata["saved_at"], "fileCount": files, "folderCount": folders}
