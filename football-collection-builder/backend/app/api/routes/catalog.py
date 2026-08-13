from fastapi import APIRouter, HTTPException, Query
from app.models.catalog import CatalogBuildRequest, CatalogBuildRun, CatalogStatus, CatalogSummary, PaginatedCatalog
from app.services.catalog_builder_service import CatalogBuilderService
router=APIRouter(); service=CatalogBuilderService()
@router.post('/catalog/build',response_model=CatalogBuildRun)
def build(request:CatalogBuildRequest):
    try:return service.build(request.replacePrevious)
    except ValueError as exc: raise HTTPException(400,detail=str(exc)) from exc
@router.get('/catalog/status',response_model=CatalogStatus)
def status(): return service.status()
@router.get('/catalog/summary',response_model=CatalogSummary)
def summary():
    value=service.repository.summary()
    if value is None: raise HTTPException(404,detail='Catálogo ainda não construído.')
    return value
@router.get('/catalog/countries',response_model=PaginatedCatalog)
def countries(search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)): return service.repository.page('countries',limit,offset,search)
@router.get('/catalog/teams',response_model=PaginatedCatalog)
def teams(countryId:int|None=None,search:str|None=None,confidence:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)): return service.repository.page('teams',limit,offset,search,countryId=countryId,confidence=confidence)
@router.get('/catalog/teams/{team_id}')
def team(team_id:int):
    value=service.repository.team_detail(team_id)
    if value is None: raise HTTPException(404,detail='Equipe não encontrada.')
    return value
@router.get('/catalog/items',response_model=PaginatedCatalog)
def items(teamId:int|None=None,collectionId:int|None=None,itemType:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)): return service.repository.page('items',limit,offset,search,teamId=teamId,collectionId=collectionId,itemType=itemType)
@router.get('/catalog/items/{item_id}')
def item(item_id:int):
    value=service.repository.item_detail(item_id)
    if value is None: raise HTTPException(404,detail='Item não encontrado.')
    return value
@router.get('/catalog/issues',response_model=PaginatedCatalog)
def issues(issueType:str|None=None,severity:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)): return service.repository.page('issues',limit,offset,search,issueType=issueType,severity=severity)
