from app.models.inventory import Inventory
from app.models.scanner import ScannerResponse
from app.services.inventory_builder import build_inventory
from app.services.scanner_service import scan_workspace


class InventoryService:
    def load(self, inventory: Inventory) -> Inventory:
        return inventory

    def create(self, workspace_path: str) -> Inventory:
        scan = scan_workspace(workspace_path)
        return build_inventory(scan)

    def get(self, inventory: Inventory) -> Inventory:
        return inventory

    def validate(self, inventory: Inventory) -> bool:
        return (
            inventory.statistics.totalFiles == len(inventory.items)
            and inventory.statistics.totalDirectories == len(inventory.folders)
            and inventory.statistics.totalSize == sum(item.size for item in inventory.items)
        )

    def from_scan(self, scan: ScannerResponse) -> Inventory:
        return build_inventory(scan)