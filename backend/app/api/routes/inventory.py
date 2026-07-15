from fastapi import APIRouter

from app.models.inventory import Inventory, InventoryRequest
from app.services.inventory_service import InventoryService

router = APIRouter()
service = InventoryService()


@router.post("/inventory/build", response_model=Inventory)
async def build_inventory_endpoint(request: InventoryRequest):
    return service.create(request.workspacePath)