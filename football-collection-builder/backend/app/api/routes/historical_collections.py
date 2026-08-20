from fastapi import APIRouter, HTTPException, Query

from app.services.historical_collections_service import HistoricalCollectionsService

router = APIRouter()
service = HistoricalCollectionsService()
ALIASES = {"flamulas": "pennants", "pennants": "pennants", "bandeiras": "flags", "flags": "flags", "memorabilia": "memorabilia"}


@router.post("/historical-collections/build")
def build():
    try:
        return service.build()
    except ValueError as exc:
        raise HTTPException(400, detail=str(exc)) from exc


@router.get("/historical-collections/status")
def status():
    return service.status()


@router.get("/public/collections/summary")
def summary():
    value = service.repository.summary()
    if value is None:
        raise HTTPException(404, detail="Coleções Históricas ainda não construídas.")
    return value


@router.get("/public/collections/sections")
def sections():
    return {"items": service.repository.sections()}


def resolve_section(section: str) -> str:
    value = ALIASES.get(section)
    if value is None:
        raise HTTPException(404, detail="Seção não encontrada.")
    return value


@router.get("/public/collections/sections/{section}")
def section(section: str):
    value = service.repository.section(resolve_section(section))
    if value is None:
        raise HTTPException(404, detail="Seção não encontrada.")
    return value


@router.get("/public/collections/sections/{section}/items")
def items(section: str, group: str | None = None, category: str | None = None,
          limit: int = Query(24, ge=1, le=100), offset: int = Query(0, ge=0)):
    return service.repository.items(resolve_section(section), limit, offset, group, category)


@router.get("/public/collections/sections/{section}/items/{slug}")
def item(section: str, slug: str):
    value = service.repository.item(resolve_section(section), slug)
    if value is None:
        raise HTTPException(404, detail="Item não encontrado.")
    return value


@router.get("/public/collections/sections/pennants/groups")
def groups():
    value = service.repository.section("pennants")
    if value is None:
        raise HTTPException(404, detail="Seção não encontrada.")
    return {"items": value["groups"]}


@router.get("/public/collections/sections/pennants/groups/{group}")
def group(group: str, limit: int = Query(24, ge=1, le=100), offset: int = Query(0, ge=0)):
    if group not in {"brasil", "italy", "other"}:
        raise HTTPException(404, detail="Grupo não encontrado.")
    return service.repository.items("pennants", limit, offset, group)
