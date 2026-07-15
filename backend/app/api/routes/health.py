from fastapi import APIRouter

from app.models.workspace import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        service="football-collection-builder-api",
        version="0.1.0-alpha",
    )
