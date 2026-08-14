from typing import Any
from pydantic import BaseModel, Field

class NormalizationRunRequest(BaseModel):
    pass

class NormalizationPage(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)
    total: int
    limit: int
    offset: int
