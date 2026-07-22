from __future__ import annotations

from time import perf_counter

from app.models.inventory import Inventory, InventoryDatabaseStatus, InventoryPersistenceResult
from app.repositories.inventory_repository import InventoryRepository


class InventoryPersistenceService:
    def __init__(self, repository: InventoryRepository | None = None):
        self.repository = repository or InventoryRepository()

    def persist(self, inventory: Inventory) -> InventoryPersistenceResult:
        if inventory.statistics.totalFiles != len(inventory.items):
            raise ValueError("A quantidade de arquivos do Inventory é inconsistente.")
        if inventory.statistics.totalDirectories != len(inventory.folders):
            raise ValueError("A quantidade de pastas do Inventory é inconsistente.")

        database_created = not self.repository.database_path.exists()
        started_at = perf_counter()
        saved_at = self.repository.save(inventory)
        duration_ms = int((perf_counter() - started_at) * 1000)
        persisted = self.repository.get_statistics()
        if persisted is None or persisted.totalFiles != inventory.statistics.totalFiles:
            raise RuntimeError("Não foi possível validar o Inventory persistido.")

        return InventoryPersistenceResult(
            success=True,
            databaseCreated=database_created,
            savedAt=saved_at,
            fileCount=inventory.statistics.totalFiles,
            folderCount=inventory.statistics.totalDirectories,
            durationMs=duration_ms,
            message="Inventory salvo com sucesso.",
        )

    def status(self) -> InventoryDatabaseStatus:
        return InventoryDatabaseStatus.model_validate(self.repository.get_status())