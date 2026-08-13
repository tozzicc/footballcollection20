from typing import Any
from pydantic import BaseModel, Field

class CatalogBuildRequest(BaseModel):
    replacePrevious: bool = True

class CatalogBuildRun(BaseModel):
    id: int | None = None
    startedAt: str
    finishedAt: str | None = None
    durationMs: int = 0
    status: str
    countries: int = 0
    teams: int = 0
    collections: int = 0
    items: int = 0
    imageRelations: int = 0
    issues: int = 0
    message: str

class CatalogStatus(BaseModel):
    inventoryAvailable: bool
    htmlParserAvailable: bool
    imageParserAvailable: bool
    catalogAvailable: bool
    lastBuild: CatalogBuildRun | None = None
    status: str

class CatalogSummary(BaseModel):
    countries: int = 0
    teams: int = 0
    collections: int = 0
    items: int = 0
    imageRelations: int = 0
    unknownCountries: int = 0
    unknownTeams: int = 0
    issues: int = 0
    duration: int = 0
    builtAt: str | None = None

class PaginatedCatalog(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)
    total: int
    limit: int
    offset: int

