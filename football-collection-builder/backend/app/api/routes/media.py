from datetime import datetime,timezone
from email.utils import format_datetime
import hashlib
from fastapi import APIRouter,HTTPException,Query,Request,Response
from fastapi.responses import FileResponse
from app.repositories.media_repository import MediaRepository
from app.services.media_resolver import MediaResolutionError,MediaResolver
from app.services.media_service import MediaService

router=APIRouter();service=MediaService();resolver=MediaResolver(service.repository)
@router.post('/media/build')
def build():
 try:
  x=service.build();return {'status':x['status'],'schemaVersion':x['schema_version'],'totalRelations':x['total_relations'],'uniqueAssets':x['unique_assets'],'availableAssets':x['available_assets'],'unavailableAssets':x['unavailable_assets'],'invalidAssets':x['invalid_assets'],'durationMs':x['duration_ms'],'completedAt':x['completed_at']}
 except ValueError as exc:raise HTTPException(400,detail=str(exc)) from exc
@router.get('/media/status')
def status():return service.status()
@router.get('/media/summary')
def summary():
 x=service.repository.summary()
 if x is None:raise HTTPException(404,detail='Media Layer ainda não preparada.')
 return x
@router.get('/media/assets')
def assets(search:str='',available:bool|None=None,format:str|None=None,limit:int=Query(24,ge=1,le=100),offset:int=Query(0,ge=0)):return service.repository.page(limit,offset,search,available,format)
@router.get('/media/assets/{media_key}/metadata')
def metadata(media_key:str):
 x=service.repository.asset(media_key)
 if x is None:raise HTTPException(404,detail='Asset não encontrado.')
 return service.repository.public_asset(x)
@router.get('/media/assets/{media_key}')
def asset(media_key:str,request:Request):
 try:x,path=resolver.resolve(media_key)
 except MediaResolutionError as exc:raise HTTPException(404,detail='Asset não encontrado.') from exc
 if not x['valid']:raise HTTPException(422,detail='Asset de imagem inválido.')
 if x['format']=='SVG':raise HTTPException(415,detail='SVG não é servido inline nesta versão.')
 modified=x['modified_at'] or datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat();etag='"'+hashlib.sha256(f"{media_key}|{x['file_size']}|{modified}".encode()).hexdigest()+'"'
 headers={'Cache-Control':'public, max-age=3600','ETag':etag,'Last-Modified':format_datetime(datetime.fromtimestamp(path.stat().st_mtime,timezone.utc),usegmt=True)}
 if request.headers.get('if-none-match')==etag:return Response(status_code=304,headers=headers)
 return FileResponse(path,media_type=x['mime_type'],headers=headers)
