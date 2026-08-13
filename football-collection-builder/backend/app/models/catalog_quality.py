from typing import Any
from pydantic import BaseModel, Field
class CatalogQualityRequest(BaseModel): replacePrevious: bool=True
class CatalogQualityRun(BaseModel):
    id:int|None=None; catalogBuildRunId:int; startedAt:str; finishedAt:str|None=None; durationMs:int=0; status:str
    totalIssues:int=0; autoResolved:int=0; reviewRequired:int=0; qualityScore:float=0; message:str
class CatalogQualityStatus(BaseModel):
    catalogAvailable:bool; qualityAnalysisAvailable:bool; catalogBuildRunId:int|None=None; lastAnalysis:CatalogQualityRun|None=None; status:str
class CatalogQualitySummary(BaseModel):
    totalIssues:int;openIssues:int;autoResolvedIssues:int;reviewRequiredIssues:int;issuesByType:dict[str,int];issuesBySeverity:dict[str,int]
    countriesTotal:int;countriesConfirmed:int;countriesInferred:int;countriesUnknown:int;teamsTotal:int;teamsConfirmed:int;teamsInferred:int;teamsUnknown:int
    itemsTotal:int;itemsConfirmed:int;itemsInferred:int;itemsUnknown:int;collectionsTotal:int;collectionsClassified:int;collectionsUnknown:int;missingImages:int
    qualityScore:float;analyzedAt:str;durationMs:int
class QualityPage(BaseModel): items:list[dict[str,Any]]=Field(default_factory=list);total:int;limit:int;offset:int
