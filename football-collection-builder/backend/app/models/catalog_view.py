from typing import Any
from pydantic import BaseModel,Field

class CatalogViewBuildRequest(BaseModel):
    replacePrevious:bool=False
class PublicPage(BaseModel):
    items:list[dict[str,Any]]=Field(default_factory=list)
    total:int;limit:int;offset:int;hasNext:bool
