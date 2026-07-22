import sqlite3
from pathlib import Path

import pytest

from app.database.schema import TABLES
from app.models.inventory import (
    Inventory,
    InventoryCategorySummary,
    InventoryExtensionSummary,
    InventoryFolder,
    InventoryItem,
    InventoryMetadata,
    InventoryStatistics,
)
from app.repositories.inventory_repository import InventoryRepository
from app.services.inventory_persistence_service import InventoryPersistenceService


def make_inventory(file_count: int = 2) -> Inventory:
    items = [
        InventoryItem(
            id=f"item-{index}", relativePath=f"cards/card-{index}.jpg", absolutePath=f"C:/collection/cards/card-{index}.jpg",
            directory="cards", filename=f"card-{index}.jpg", extension=".jpg", category="images", size=10 + index,
            createdAt="2026-01-01T00:00:00Z", modifiedAt="2026-01-02T00:00:00Z", readable=True,
        )
        for index in range(file_count)
    ]
    return Inventory(
        metadata=InventoryMetadata(generatedAt="2026-01-03T00:00:00Z", scannerVersion="1.1", workspacePath="C:/collection", durationMs=25),
        statistics=InventoryStatistics(totalFiles=file_count, totalDirectories=2, totalSize=sum(item.size for item in items), totalImages=file_count, totalPages=0, totalVideos=0, totalDocuments=0, totalArchives=0, totalData=0, totalOther=0),
        folders=[
            InventoryFolder(path="C:/collection", relativePath=".", name="collection", parent=None, depth=0),
            InventoryFolder(path="C:/collection/cards", relativePath="cards", name="cards", parent=".", depth=1),
        ],
        items=items,
        categories=[InventoryCategorySummary(category="images", count=file_count), InventoryCategorySummary(category="other", count=0)],
        extensions=[InventoryExtensionSummary(extension=".jpg", count=file_count)],
        errors=[],
    )


def test_database_is_created_automatically(tmp_path: Path):
    path = tmp_path / "nested" / "football_collection.db"
    repository = InventoryRepository(path)
    assert not path.exists()
    repository.save(make_inventory())
    assert path.exists()


def test_schema_creates_all_inventory_tables_and_indexes(tmp_path: Path):
    repository = InventoryRepository(tmp_path / "inventory.db")
    repository.create_schema()
    assert set(repository.schema_tables()) == set(TABLES)
    with repository.database.connect() as connection:
        indexes = {row["name"] for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'index'")}
    assert {"idx_inventory_folders_relative_path", "idx_inventory_items_relative_path", "idx_inventory_items_extension", "idx_inventory_items_category", "idx_inventory_items_directory"}.issubset(indexes)


def test_complete_inventory_persistence(tmp_path: Path):
    repository = InventoryRepository(tmp_path / "inventory.db")
    inventory = make_inventory()
    repository.save(inventory)
    loaded = repository.get_inventory()
    assert loaded is not None
    assert loaded.statistics == inventory.statistics
    assert len(loaded.items) == 2
    assert len(loaded.folders) == 2


def test_transaction_rolls_back_on_error(tmp_path: Path, monkeypatch):
    repository = InventoryRepository(tmp_path / "inventory.db")
    repository.save(make_inventory(1))
    def fail_items(connection: sqlite3.Connection, values: list[InventoryItem]) -> None:
        raise sqlite3.DatabaseError("forced failure")
    monkeypatch.setattr(repository, "_insert_items", fail_items)
    with pytest.raises(sqlite3.DatabaseError, match="forced failure"):
        repository.save(make_inventory(2))
    assert repository.get_statistics().totalFiles == 1
    assert len(repository.get_first_items()) == 1


def test_statistics_query(tmp_path: Path):
    repository = InventoryRepository(tmp_path / "inventory.db")
    repository.save(make_inventory(2))
    assert repository.get_statistics().totalSize == 21


def test_extensions_query(tmp_path: Path):
    repository = InventoryRepository(tmp_path / "inventory.db")
    repository.save(make_inventory())
    assert repository.get_extensions() == [InventoryExtensionSummary(extension=".jpg", count=2)]


def test_categories_query(tmp_path: Path):
    repository = InventoryRepository(tmp_path / "inventory.db")
    repository.save(make_inventory())
    assert {value.category: value.count for value in repository.get_categories()} == {"images": 2, "other": 0}


def test_first_files_query_respects_limit(tmp_path: Path):
    repository = InventoryRepository(tmp_path / "inventory.db")
    repository.save(make_inventory(2))
    files = repository.get_first_items(limit=1)
    assert len(files) == 1
    assert files[0].relativePath == "cards/card-0.jpg"


def test_rewrite_replaces_previous_inventory_without_duplicates(tmp_path: Path):
    repository = InventoryRepository(tmp_path / "inventory.db")
    repository.save(make_inventory(2))
    repository.save(make_inventory(1))
    assert repository.get_statistics().totalFiles == 1
    assert len(repository.get_first_items()) == 1


def test_persistence_service_returns_counts_and_status(tmp_path: Path):
    service = InventoryPersistenceService(InventoryRepository(tmp_path / "inventory.db"))
    result = service.persist(make_inventory())
    status = service.status()
    assert result.success is True
    assert result.fileCount == 2
    assert result.folderCount == 2
    assert result.durationMs >= 0
    assert status.databaseCreated is True
    assert status.fileCount == 2
    assert status.folderCount == 2