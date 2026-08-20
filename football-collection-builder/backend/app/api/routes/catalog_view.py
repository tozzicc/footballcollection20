from fastapi import APIRouter,HTTPException,Query
from app.models.catalog_view import CatalogViewBuildRequest,PublicPage
from app.services.catalog_view_service import CatalogViewService

router=APIRouter();service=CatalogViewService()
@router.post('/public/catalog/build')
def build(_:CatalogViewBuildRequest):
 try:
  result=service.build()
  return {'status':result['status'],'schemaVersion':result['schema_version'],'countries':result['countries'],'teams':result['teams'],'collections':result['collections'],'items':result['items'],'mediaRelations':result['media_relations'],'ready':result['ready'],'reviewRequired':result['review_required'],'unavailable':result['unavailable'],'durationMs':result['duration_ms'],'completedAt':result['completed_at']}
 except ValueError as exc:raise HTTPException(400,detail=str(exc)) from exc
@router.get('/public/catalog/status')
def status():return service.status()
@router.get('/public/catalog/summary')
def summary():
 value=service.repository.summary()
 if value is None:raise HTTPException(404,detail='Modelo público ainda não gerado.')
 return value
def page(kind,limit,offset,**filters):return service.repository.page(kind,limit,offset,filters)
@router.get('/public/catalog/countries',response_model=PublicPage)
def countries(search:str|None=None,status:str|None=None,limit:int=Query(24,ge=1,le=100),offset:int=Query(0,ge=0)):return page('countries',limit,offset,search=search,status=status)
@router.get('/public/catalog/countries/{country_slug}')
def country(country_slug:str):
 value=service.repository.country_detail(country_slug)
 if value is None:raise HTTPException(404,detail='País/região não encontrado.')
 return value
@router.get('/public/catalog/teams',response_model=PublicPage)
def teams(country:str|None=None,search:str|None=None,status:str|None=None,limit:int=Query(24,ge=1,le=100),offset:int=Query(0,ge=0)):return page('teams',limit,offset,country=country,search=search,status=status)
@router.get('/public/catalog/teams/{country_slug}/{team_slug}')
def team(country_slug:str,team_slug:str):
 value=service.repository.team_detail(country_slug,team_slug)
 if value is None:raise HTTPException(404,detail='Equipe não encontrada.')
 return value
@router.get('/public/catalog/seasons/{country_slug}/{team_slug}/{season}')
def season(country_slug:str,team_slug:str,season:str):
 value=service.repository.season_detail(country_slug,team_slug,season)
 if value is None:raise HTTPException(404,detail='Temporada não encontrada.')
 return value
@router.get('/public/catalog/collections',response_model=PublicPage)
def collections(country:str|None=None,team:str|None=None,year:int|None=None,month:int|None=None,type:str|None=None,status:str|None=None,search:str|None=None,limit:int=Query(24,ge=1,le=100),offset:int=Query(0,ge=0)):return page('collections',limit,offset,country=country,team=team,year=year,month=month,type=type,status=status,search=search)
@router.get('/public/catalog/collections/{country_slug}/{team_slug}/{collection_slug}')
def collection(country_slug:str,team_slug:str,collection_slug:str):
 value=service.repository.collection_detail(country_slug,team_slug,collection_slug)
 if value is None:raise HTTPException(404,detail='Collection não encontrada.')
 return value
@router.get('/public/catalog/items',response_model=PublicPage)
def items(country:str|None=None,team:str|None=None,collection:str|None=None,itemType:str|None=None,status:str|None=None,search:str|None=None,limit:int=Query(24,ge=1,le=100),offset:int=Query(0,ge=0)):return page('items',limit,offset,country=country,team=team,collection=collection,itemType=itemType,status=status,search=search)
@router.get('/public/catalog/items/{country_slug}/teams/{team_slug}/collections/{collection_slug}/{item_slug}')
def item_with_collection(country_slug:str,team_slug:str,collection_slug:str,item_slug:str):
 value=service.repository.item_detail(country_slug,team_slug,item_slug,collection_slug)
 if value is None:raise HTTPException(404,detail='Item não encontrado.')
 return value
@router.get('/public/catalog/items/{country_slug}/teams/{team_slug}/items/{item_slug}')
def item_without_collection(country_slug:str,team_slug:str,item_slug:str):
 value=service.repository.item_detail(country_slug,team_slug,item_slug)
 if value is None:raise HTTPException(404,detail='Item não encontrado.')
 return value
@router.get('/public/catalog/navigation')
def navigation():return service.repository.navigation()
@router.get('/public/catalog/search',response_model=PublicPage)
def search(q:str='',type:str|None=None,country:str|None=None,limit:int=Query(24,ge=1,le=100),offset:int=Query(0,ge=0)):return service.repository.search(q,type,country,limit,offset)
@router.get('/public/catalog/latest')
def latest(limit:int=Query(12,ge=1,le=100),country:str|None=None,team:str|None=None):return {'items':service.repository.latest(limit,country,team)}
