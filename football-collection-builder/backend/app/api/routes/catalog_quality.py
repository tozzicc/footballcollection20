from fastapi import APIRouter,HTTPException,Query
from app.models.catalog_quality import *
from app.services.catalog_quality_service import CatalogQualityService
router=APIRouter();service=CatalogQualityService()
@router.post('/catalog/quality/analyze',response_model=CatalogQualityRun)
def analyze(request:CatalogQualityRequest):
 try:return service.analyze(request.replacePrevious)
 except ValueError as e:raise HTTPException(400,detail=str(e)) from e
@router.get('/catalog/quality/status',response_model=CatalogQualityStatus)
def status():return service.status()
@router.get('/catalog/quality/summary',response_model=CatalogQualitySummary)
def summary():
 v=service.summary()
 if v is None:raise HTTPException(404,detail='Análise de qualidade ainda não executada.')
 return v
@router.get('/catalog/quality/issues',response_model=QualityPage)
def issues(issueType:str|None=None,severity:str|None=None,resolutionStatus:str|None=None,teamId:int|None=None,countryId:int|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return service.repository.page('issues',limit,offset,issueType=issueType,severity=severity,resolutionStatus=resolutionStatus,teamId=teamId,countryId=countryId,search=search)
@router.get('/catalog/quality/issues/{issue_id}')
def detail(issue_id:int):
 v=service.repository.detail(issue_id)
 if v is None:raise HTTPException(404,detail='Issue não encontrado.')
 return v
@router.get('/catalog/quality/resolutions',response_model=QualityPage)
def resolutions(ruleCode:str|None=None,resolutionType:str|None=None,confidence:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return service.repository.page('resolutions',limit,offset,ruleCode=ruleCode,resolutionType=resolutionType,confidence=confidence)
@router.get('/catalog/quality/groups')
def groups():return service.repository.groups()
