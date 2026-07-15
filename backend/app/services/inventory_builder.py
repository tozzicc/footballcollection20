from __future__ import annotations

from datetime import datetime, timezone
from uuid import NAMESPACE_URL, uuid5

from app.models.inventory import (
    Inventory,
    InventoryCategorySummary,
    InventoryExtensionSummary,
    InventoryFolder,
    InventoryItem,
    InventoryMetadata,
    InventoryStatistics,
)
from app.models.scanner import ScannerResponse

SCANNER_VERSION = "1.1"


def _generated_at() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_inventory(scan: ScannerResponse) -> Inventory:
    """Transform a Scanner response without accessing the filesystem."""
    items = [
        InventoryItem(
            id=str(uuid5(NAMESPACE_URL, f"{scan.workspacePath}:{item.relativePath}")),
            relativePath=item.relativePath,
            absolutePath=item.absolutePath,
            directory=item.directory,
            filename=item.filename,
            extension=item.extension,
            category=item.category,
            size=item.size,
            createdAt=item.createdAt,
            modifiedAt=item.modifiedAt,
            readable=item.readable,
        )
        for item in scan.files
    ]
    folders = [
        InventoryFolder(
            path=folder.absolutePath,
            relativePath=folder.relativePath,
            name=folder.name,
            parent=folder.parent,
            depth=folder.depth,
        )
        for folder in scan.folders
    ]
    category_values = {
        "images": scan.categories.images,
        "pages": scan.categories.pages,
        "videos": scan.categories.videos,
        "documents": scan.categories.documents,
        "archives": scan.categories.archives,
        "data": scan.categories.data,
        "audio": scan.categories.audio,
        "other": scan.categories.other,
    }
    statistics = InventoryStatistics(
        totalFiles=scan.totalFiles,
        totalDirectories=scan.totalDirectories,
        totalSize=scan.totalBytes,
        totalImages=scan.categories.images,
        totalPages=scan.categories.pages,
        totalVideos=scan.categories.videos,
        totalDocuments=scan.categories.documents,
        totalArchives=scan.categories.archives,
        totalData=scan.categories.data,
        totalOther=scan.categories.other,
    )
    return Inventory(
        metadata=InventoryMetadata(
            generatedAt=_generated_at(),
            scannerVersion=SCANNER_VERSION,
            workspacePath=scan.workspacePath,
            durationMs=scan.durationMs,
        ),
        statistics=statistics,
        folders=folders,
        items=items,
        categories=[InventoryCategorySummary(category=name, count=count) for name, count in category_values.items()],
        extensions=[InventoryExtensionSummary(extension=item.extension, count=item.count) for item in scan.extensions],
        errors=list(scan.errors),
    )