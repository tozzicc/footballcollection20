from fastapi import APIRouter,HTTPException,Query
from app.models.catalog_normalization import NormalizationPage,NormalizationRunRequest
from app.services.catalog_normalization_service import CatalogNormalizationService

router=APIRouter();service=CatalogNormalizationService()
@router.get('/catalog/normalization/status')
def status():return service.status()
@router.post('/catalog/normalization/run')
def run(_:NormalizationRunRequest):
    try:return service.run()
    except ValueError as exc:raise HTTPException(400,detail=str(exc)) from exc
@router.get('/catalog/normalization/summary')
def summary():
    value=service.repository.summary()
    if value is None:raise HTTPException(404,detail='Normalização ainda não executada.')
    return value
def page(kind,limit,offset,**filters):return service.repository.page(kind,limit,offset,filters)
@router.get('/catalog/normalization/countries',response_model=NormalizationPage)
def countries(status:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return page('countries',limit,offset,status=status,search=search)
@router.get('/catalog/normalization/teams',response_model=NormalizationPage)
def teams(country:str|None=None,status:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return page('teams',limit,offset,country=country,status=status,search=search)
@router.get('/catalog/normalization/collections',response_model=NormalizationPage)
def collections(country:str|None=None,team:str|None=None,type:str|None=None,status:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return page('collections',limit,offset,country=country,team=team,type=type,status=status,search=search)
@router.get('/catalog/normalization/items',response_model=NormalizationPage)
def items(country:str|None=None,team:str|None=None,collection:str|None=None,status:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return page('items',limit,offset,country=country,team=team,collection=collection,status=status,search=search)
@router.get('/catalog/normalization/events',response_model=NormalizationPage)
def events(entityType:str|None=None,ruleCode:str|None=None,status:str|None=None,source:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return service.repository.events(limit,offset,locals())
@router.get('/catalog/normalization/{kind}/{stable_key:path}')
def detail(kind:str,stable_key:str):
    if kind not in ('countries','teams','collections','items'):raise HTTPException(404,detail='Tipo não encontrado.')
    value=service.repository.detail(kind,stable_key)
    if value is None:raise HTTPException(404,detail='Entidade normalizada não encontrada.')
    return value
