from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class HtmlParseStatus(str, Enum):
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"


class HtmlReferenceStatus(str, Enum):
    RESOLVED = "resolved"
    MISSING = "missing"
    EXTERNAL = "external"
    ANCHOR = "anchor"
    IGNORED = "ignored"
    INVALID = "invalid"


class HtmlParseRequest(BaseModel):
    workspacePath: str
    replacePrevious: bool = True

    @field_validator("workspacePath")
    @classmethod
    def workspace_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("workspacePath cannot be empty")
        return value.strip()


class HtmlHeading(BaseModel):
    level: int
    position: int
    text: str


class HtmlReference(BaseModel):
    original: str
    normalized: str
    isExternal: bool
    resolvedRelativePath: str | None = None
    existsInInventory: bool = False
    referencedInventoryItemId: str | None = None
    status: HtmlReferenceStatus


class HtmlImageReference(BaseModel):
    srcOriginal: str
    srcNormalized: str
    alt: str | None = None
    title: str | None = None
    widthDeclared: str | None = None
    heightDeclared: str | None = None
    isExternal: bool
    resolvedRelativePath: str | None = None
    resolvedAbsolutePath: str | None = None
    existsInInventory: bool = False
    referencedInventoryItemId: str | None = None
    status: HtmlReferenceStatus


class HtmlLinkReference(BaseModel):
    hrefOriginal: str
    hrefNormalized: str
    visibleText: str | None = None
    title: str | None = None
    isExternal: bool
    isAnchor: bool = False
    isMailto: bool = False
    isJavascript: bool = False
    resolvedRelativePath: str | None = None
    existsInInventory: bool = False
    referencedInventoryItemId: str | None = None
    status: HtmlReferenceStatus


class HtmlPageMetadata(BaseModel):
    inventoryItemId: str
    relativePath: str
    absolutePath: str
    filename: str
    extension: str
    fileSize: int
    createdAt: str | None = None
    modifiedAt: str | None = None
    encodingUsed: str | None = None
    title: str
    documentLanguage: str | None = None
    charsetDeclared: str | None = None
    metaDescription: str | None = None
    textPreview: str = ""
    parseStatus: str
    parseMessage: str


class HtmlPageResult(HtmlPageMetadata):
    id: int | None = None
    headings: list[HtmlHeading] = Field(default_factory=list)
    imageReferences: list[HtmlImageReference] = Field(default_factory=list)
    linkReferences: list[HtmlLinkReference] = Field(default_factory=list)


class HtmlParseError(BaseModel):
    inventoryItemId: str | None = None
    relativePath: str
    errorType: str
    message: str


class HtmlParseRun(BaseModel):
    id: int | None = None
    workspacePath: str
    startedAt: str
    finishedAt: str | None = None
    durationMs: int = 0
    status: HtmlParseStatus
    totalPages: int = 0
    parsedPages: int = 0
    failedPages: int = 0
    imageReferences: int = 0
    internalLinks: int = 0
    externalLinks: int = 0
    missingReferences: int = 0
    message: str


class HtmlParseSummary(HtmlParseRun):
    pass


class HtmlParseResponse(HtmlParseRun):
    runId: int
    errors: list[HtmlParseError] = Field(default_factory=list)


class HtmlParserStatus(BaseModel):
    hasRun: bool
    inventoryAvailable: bool
    availablePages: int = 0
    lastRun: HtmlParseSummary | None = None


class HtmlPageListItem(BaseModel):
    id: int
    relativePath: str
    filename: str
    title: str
    encodingUsed: str | None = None
    imageReferences: int
    linkReferences: int
    missingReferences: int
    parseStatus: str


class HtmlPagesResponse(BaseModel):
    items: list[HtmlPageListItem]
    total: int
    limit: int
    offset: int


class HtmlPageDetails(HtmlPageResult):
    errors: list[HtmlParseError] = Field(default_factory=list)


class HtmlMissingReference(BaseModel):
    id: int
    pageId: int
    sourceRelativePath: str
    referenceType: Literal["image", "link"]
    original: str
    resolvedRelativePath: str | None = None
    status: HtmlReferenceStatus


class HtmlMissingReferencesResponse(BaseModel):
    items: list[HtmlMissingReference]
    total: int
    limit: int
    offset: int
