from fastapi import APIRouter

from app.models.inventory import (
    Inventory,
    InventoryCategorySummary,
    InventoryDatabaseStatus,
    InventoryExtensionSummary,
    InventoryPersistenceResult,
    InventoryRequest,
    InventoryStatistics,
)
from app.services.inventory_persistence_service import InventoryPersistenceService
from app.services.inventory_service import InventoryService

router = APIRouter()
service = InventoryService()
persistence_service = InventoryPersistenceService()


@router.post("/inventory/build", response_model=Inventory)
async def build_inventory_endpoint(request: InventoryRequest):
    return service.create(request.workspacePath)

@router.post("/inventory/save", response_model=InventoryPersistenceResult)
async def save_inventory_endpoint(inventory: Inventory):
    return persistence_service.persist(inventory)


@router.get("/inventory/statistics", response_model=InventoryStatistics | None)
async def get_inventory_statistics():
    return persistence_service.repository.get_statistics()


@router.get("/inventory/extensions", response_model=list[InventoryExtensionSummary])
async def get_inventory_extensions():
    return persistence_service.repository.get_extensions()


@router.get("/inventory/categories", response_model=list[InventoryCategorySummary])
async def get_inventory_categories():
    return persistence_service.repository.get_categories()


@router.get("/inventory/status", response_model=InventoryDatabaseStatus)
async def get_inventory_status():
    return persistence_service.status()