from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.api.routes.health import router as health_router
from app.api.routes.html_parser import router as html_parser_router
from app.api.routes.image_parser import router as image_parser_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.scanner import router as scanner_router
from app.api.routes.workspace import router as workspace_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.catalog_quality import router as catalog_quality_router
from app.api.routes.catalog_review import router as catalog_review_router
from app.api.routes.catalog_normalization import router as catalog_normalization_router
from app.api.routes.catalog_view import router as catalog_view_router
from app.api.routes.media import router as media_router
from app.api.routes.historical_collections import router as historical_collections_router

app = FastAPI(title="Football Collection Builder API", version="0.1.0-alpha")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(health_router, prefix="/api")
app.include_router(html_parser_router, prefix="/api")
app.include_router(image_parser_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(workspace_router, prefix="/api")
app.include_router(scanner_router, prefix="/api")
app.include_router(catalog_router, prefix="/api")
app.include_router(catalog_quality_router, prefix="/api")
app.include_router(catalog_review_router, prefix="/api")
app.include_router(catalog_normalization_router, prefix="/api")
app.include_router(catalog_view_router, prefix="/api")
app.include_router(media_router, prefix="/api")
app.include_router(historical_collections_router, prefix="/api")


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    app.logger = getattr(app, 'logger', None)
    if app.logger is None:
        import logging

        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        app.logger = logging.getLogger("football-collection-builder-api")

    app.logger.exception("Unhandled exception while handling request")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Ocorreu um erro interno no servidor. Tente novamente mais tarde.",
        },
    )
