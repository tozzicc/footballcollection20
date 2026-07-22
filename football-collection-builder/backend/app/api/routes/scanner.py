from fastapi import APIRouter

from app.models.scanner import ScannerRequest, ScannerResponse
from app.services.scanner_service import scan_workspace_request

router = APIRouter()


@router.post("/scanner/scan", response_model=ScannerResponse)
async def scan_workspace_endpoint(request: ScannerRequest):
    return scan_workspace_request(request)
