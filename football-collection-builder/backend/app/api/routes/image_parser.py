from fastapi import APIRouter, HTTPException, Query
from app.models.image_parser import *
from app.services.image_parser_service import ImageParserService
router=APIRouter(); service=ImageParserService()
@router.post('/image-parser/parse',response_model=ImageParserResponse)
def parse(request: ImageParseRequest):
    try: return service.parse(request)
    except ValueError as exc: raise HTTPException(400,detail=str(exc)) from exc
@router.get('/image-parser/status',response_model=ImageParserStatus)
def status(): return service.status()
@router.get('/image-parser/summary',response_model=ImageParseSummary)
def summary():
    value=service.repository.latest()
    if value is None: raise HTTPException(404,detail='Nenhuma execucao concluida.')
    return value
@router.get('/image-parser/images',response_model=PaginatedImages)
def images(limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0),search:str|None=None,status:str|None=None,format:str|None=None,minWidth:int|None=Query(None,ge=0),minHeight:int|None=Query(None,ge=0)): return service.repository.images(limit,offset,search,status,format,minWidth,minHeight)
@router.get('/image-parser/images/{image_id}',response_model=ImageMetadata)
def detail(image_id:int):
    value=service.repository.detail(image_id)
    if value is None: raise HTTPException(404,detail='Imagem nao encontrada.')
    return value
@router.get('/image-parser/orphans',response_model=PaginatedImages)
def orphans(limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)): return service.repository.images(limit,offset,kind='orphan')
@router.get('/image-parser/invalid',response_model=PaginatedImages)
def invalid(limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)): return service.repository.images(limit,offset,kind='invalid')
@router.get('/image-parser/broken-references',response_model=PaginatedBrokenReferences)
def broken(limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)): return service.repository.broken(limit,offset)
