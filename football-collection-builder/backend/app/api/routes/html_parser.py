from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from app.models.html_parser import (
    HtmlMissingReferencesResponse, HtmlPageDetails, HtmlPagesResponse, HtmlParseRequest,
    HtmlParseResponse, HtmlParserStatus, HtmlParseSummary,
)
from app.services.html_parser_service import HtmlParserService

router = APIRouter()
service = HtmlParserService()


@router.post("/html-parser/parse", response_model=HtmlParseResponse)
async def parse_html(request: HtmlParseRequest):
    try:
        return service.parse(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/html-parser/status", response_model=HtmlParserStatus)
async def parser_status():
    return service.status()


@router.get("/html-parser/summary", response_model=HtmlParseSummary)
async def parser_summary():
    result = service.repository.get_latest_run(completed_only=True)
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhuma execucao concluida.")
    return result


@router.get("/html-parser/pages", response_model=HtmlPagesResponse)
async def parser_pages(
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
    status: str | None = None, search: str | None = None,
):
    return service.repository.get_pages(limit, offset, status, search)


@router.get("/html-parser/pages/{page_id}", response_model=HtmlPageDetails)
async def parser_page(page_id: int):
    result = service.repository.get_page(page_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Pagina nao encontrada.")
    return result


@router.get("/html-parser/missing-references", response_model=HtmlMissingReferencesResponse)
async def missing_references(
    limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
    referenceType: Literal["image", "link"] | None = None,
):
    return service.repository.get_missing_references(limit, offset, referenceType)
