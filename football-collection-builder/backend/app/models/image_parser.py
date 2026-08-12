from enum import Enum
from pydantic import BaseModel, Field, field_validator

class ImageReferenceStatus(str, Enum):
    REFERENCED = "referenced"
    ORPHAN = "orphan"
    UNRESOLVED_CONTEXT = "unresolved-context"

class ImageParseRequest(BaseModel):
    workspacePath: str
    replacePrevious: bool = True
    @field_validator("workspacePath")
    @classmethod
    def workspace_not_empty(cls, value: str) -> str:
        if not value.strip(): raise ValueError("workspacePath cannot be empty")
        return value.strip()

class ImageParseError(BaseModel):
    inventoryItemId: str | None = None
    relativePath: str
    errorType: str
    message: str

class ImageMetadata(BaseModel):
    id: int | None = None
    inventoryItemId: str; relativePath: str; absolutePath: str; filename: str; extension: str
    format: str | None = None; fileSize: int; width: int | None = None; height: int | None = None
    aspectRatio: float | None = None; mode: str | None = None; hasAlpha: bool = False
    animated: bool = False; frameCount: int = 1; dpiX: float | None = None; dpiY: float | None = None
    createdAt: str | None = None; modifiedAt: str | None = None; readable: bool
    validImage: bool; validationStatus: str; validationMessage: str
    referenceCount: int = 0; referenceStatus: ImageReferenceStatus

class ImageTechnicalMetadata(ImageMetadata): pass

class ImageParseRun(BaseModel):
    id: int | None = None; workspacePath: str; startedAt: str; finishedAt: str | None = None
    durationMs: int = 0; status: str; totalImages: int = 0; validImages: int = 0
    invalidImages: int = 0; referencedImages: int = 0; orphanImages: int = 0
    brokenReferences: int = 0; htmlAuditAvailable: bool = False; totalSize: int = 0
    averageWidth: float | None = None; averageHeight: float | None = None
    maxWidth: int | None = None; maxHeight: int | None = None; formats: dict[str, int] = Field(default_factory=dict)
    message: str

class ImageParseSummary(ImageParseRun): pass
class ImageParserStatus(BaseModel):
    hasRun: bool; inventoryAvailable: bool; htmlParserAvailable: bool; availableImages: int = 0
    lastRun: ImageParseSummary | None = None
class ImageParserResponse(ImageParseRun):
    runId: int; errors: list[ImageParseError] = Field(default_factory=list)
class PaginatedImages(BaseModel):
    items: list[ImageMetadata]; total: int; limit: int; offset: int
class OrphanImage(ImageMetadata): pass
class BrokenImageReference(BaseModel):
    id: int; pageId: int; pageRelativePath: str; referenceOriginal: str
    resolvedRelativePath: str | None = None; status: str
class PaginatedBrokenReferences(BaseModel):
    items: list[BrokenImageReference]; total: int; limit: int; offset: int
