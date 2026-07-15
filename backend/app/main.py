from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.api.routes.health import router as health_router
from app.api.routes.workspace import router as workspace_router

app = FastAPI(title="Football Collection Builder API", version="0.1.0-alpha")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(health_router, prefix="/api")
app.include_router(workspace_router, prefix="/api")


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
