from fastapi import APIRouter,HTTPException,Query
from app.models.catalog_review import ReviewResolveRequest,ReviewReasonRequest
from app.services.catalog_manual_review_service import CatalogManualReviewService
router=APIRouter();service=CatalogManualReviewService()
def call(fn,*args):
 try:return fn(*args)
 except ValueError as e:raise HTTPException(400,detail=str(e)) from e
@router.get('/catalog/review/status')
def status():return service.status()
@router.get('/catalog/review/summary')
def summary():return call(service.repository.summary)
@router.get('/catalog/review/issues')
def issues(issueType:str|None=None,severity:str|None=None,status:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return service.repository.queue(limit,offset,{'issueType':issueType,'severity':severity,'status':status,'search':search})
@router.get('/catalog/review/issues/{issue_id}')
def detail(issue_id:int):return call(service.context,issue_id)
@router.get('/catalog/review/issues/{issue_id}/candidates')
def candidates(issue_id:int,search:str='',limit:int=Query(20,ge=1,le=100)):return call(service.candidates,issue_id,search,limit)
@router.post('/catalog/review/issues/{issue_id}/preview')
def preview(issue_id:int,request:ReviewResolveRequest):return call(service.preview,issue_id,request)
@router.post('/catalog/review/issues/{issue_id}/resolve')
def resolve(issue_id:int,request:ReviewResolveRequest):return call(service.resolve,issue_id,request)
@router.post('/catalog/review/issues/{issue_id}/acknowledge')
def acknowledge(issue_id:int,request:ReviewReasonRequest):return call(service.acknowledge,issue_id,request.reason)
@router.post('/catalog/review/issues/{issue_id}/defer')
def defer(issue_id:int,request:ReviewReasonRequest):return call(service.defer,issue_id,request.reason)
@router.post('/catalog/review/issues/{issue_id}/revert')
def revert(issue_id:int):return call(service.revert,issue_id)
@router.get('/catalog/review/history')
def history(status:str|None=None,resolutionCode:str|None=None,issueType:str|None=None,search:str|None=None,limit:int=Query(50,ge=1,le=200),offset:int=Query(0,ge=0)):return service.repository.history(limit,offset,{'status':status,'resolutionCode':resolutionCode,'issueType':issueType,'search':search})
