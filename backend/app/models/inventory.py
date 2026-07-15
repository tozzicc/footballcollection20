from pydantic import BaseModel

from app.models.scanner import ScanError


class InventoryItem(BaseModel):
    id: str
    relativePath: str
    absolutePath: str
    directory: str
    filename: str
    extension: str
    category: str
    size: int
    createdAt: str | None = None
    modifiedAt: str | None = None
    isDirectory: bool = False
    readable: bool


class InventoryFolder(BaseModel):
    path: str
    relativePath: str
    name: str
    parent: str | None = None
    depth: int


class InventoryStatistics(BaseModel):
    totalFiles: int
    totalDirectories: int
    totalSize: int
    totalImages: int
    totalPages: int
    totalVideos: int
    totalDocuments: int
    totalArchives: int
    totalData: int
    totalOther: int


class InventoryCategorySummary(BaseModel):
    category: str
    count: int


class InventoryExtensionSummary(BaseModel):
    extension: str
    count: int


class InventoryMetadata(BaseModel):
    generatedAt: str
    scannerVersion: str
    workspacePath: str
    durationMs: int


class Inventory(BaseModel):
    metadata: InventoryMetadata
    statistics: InventoryStatistics
    folders: list[InventoryFolder]
    items: list[InventoryItem]
    categories: list[InventoryCategorySummary]
    extensions: list[InventoryExtensionSummary]
    errors: list[ScanError]


class InventoryRequest(BaseModel):
    workspacePath: str