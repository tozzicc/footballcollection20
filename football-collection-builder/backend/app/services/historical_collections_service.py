from __future__ import annotations

import hashlib
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup, Tag

from app.repositories.historical_collections_repository import HistoricalCollectionsRepository

COLLECTIONS_SCHEMA_VERSION = "1.0.0"
SOURCES = {
    "pennants": (("pennants/brasil.htm", "brasil"), ("pennants/italy.htm", "italy"), ("pennants/other.htm", "other")),
    "flags": (("flags/flags.htm", None),),
    "memorabilia": (("memorabilia/memorabilia.htm", None),),
}
SECTION_DATA = {
    "pennants": ("Flâmulas", "Flâmulas históricas organizadas nos grupos originais Brasil, Itália e Outros."),
    "flags": ("Bandeiras", "Bandeiras, faixas e objetos físicos preservados pelo acervo."),
    "memorabilia": ("Memorabilia", "Objetos e lembranças históricas ligados ao futebol."),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-") or "item-historico"


def clean_text(value: str) -> str:
    return " ".join(value.replace("\r", " ").replace("\n", " ").split())


class HistoricalCollectionsService:
    def __init__(self, repository=None):
        self.repository = repository or HistoricalCollectionsRepository()

    @staticmethod
    def _read(path: Path) -> BeautifulSoup:
        raw = path.read_bytes()
        return BeautifulSoup(raw.decode("iso-8859-1"), "html.parser")

    @staticmethod
    def _pennant_caption(image: Tag) -> str | None:
        cell = image.find_parent("td")
        row = cell.find_parent("tr") if cell else None
        if not row:
            return None
        cells = row.find_all("td", recursive=False)
        try:
            index = cells.index(cell)
        except ValueError:
            return None
        caption_row = row.find_next_sibling("tr")
        if not caption_row:
            return None
        captions = caption_row.find_all("td", recursive=False)
        return clean_text(captions[index].get_text(" ", strip=True)) if index < len(captions) else None

    @staticmethod
    def _sibling_caption(image: Tag, direction: str) -> str | None:
        table = image.find_parent("table")
        sibling = getattr(table, f"find_{direction}_sibling")() if table else None
        while sibling:
            if isinstance(sibling, Tag):
                text = clean_text(sibling.get_text(" ", strip=True))
                if text:
                    return text
            sibling = getattr(sibling, f"find_{direction}_sibling")()
        return None

    @staticmethod
    def _category(title: str | None) -> str | None:
        value = (title or "").upper()
        rules = (("GUANT", "luvas"), ("FASCIA", "bracadeiras"), ("CALZE", "meias"),
                 ("SCARP", "chuteiras"), ("PALLON", "bolas"), ("PALLA", "bolas"))
        return next((category for token, category in rules if token in value), None)

    def _extract(self, root: Path, section: str, source: str, group: str | None, lookup: dict) -> list[dict]:
        soup = self._read(root / Path(*source.split("/")))
        items = []
        for order, image in enumerate(soup.find_all("img"), 1):
            src = unquote(image.get("src", "").split("?", 1)[0].split("#", 1)[0]).replace("\\", "/")
            relative = (Path(source).parent / Path(*src.split("/"))).as_posix()
            metadata = lookup.get(relative.casefold())
            if metadata is None:
                raise ValueError(f"Image Metadata ausente para referência editorial: {relative}")
            if section == "pennants":
                title = self._pennant_caption(image)
            elif section == "flags":
                title = self._sibling_caption(image, "previous")
            else:
                title = self._sibling_caption(image, "next")
            title = clean_text(title) if title else None
            identity = f"{section}|{source}|{order}|{relative.casefold()}"
            stable_key = hashlib.sha256(identity.encode("utf-8")).hexdigest()
            status = "unavailable" if not metadata["valid_image"] or not metadata["readable"] else "ready" if title else "review_required"
            items.append({
                "section": section, "group_key": group, "title": title, "description": title,
                "category": self._category(title) if section == "memorabilia" else None,
                "slug": f"{slugify(title or 'item-historico')}-{stable_key[:8]}", "stable_key": stable_key,
                "source_html": source, "source_order": order, "status": status,
                "media": {"inventory_reference": metadata["inventory_item_id"], "relative_path": metadata["relative_path"],
                          "display_order": 1, "is_primary": 1, "media_role": "primary", "status": status},
            })
        return items

    def build(self) -> dict:
        self.repository.create_schema()
        workspace = self.repository.workspace()
        if not workspace:
            raise ValueError("Workspace persistido necessário.")
        root = Path(workspace).resolve()
        lookup = self.repository.image_lookup()
        started = utc_now()
        clock = time.perf_counter()
        items = []
        for section, sources in SOURCES.items():
            for source, group in sources:
                path = (root / Path(*source.split("/"))).resolve()
                try:
                    path.relative_to(root)
                except ValueError as exc:
                    raise ValueError("Fonte histórica fora do Workspace.") from exc
                if not path.is_file():
                    raise ValueError(f"Fonte histórica ausente: {source}")
                items.extend(self._extract(root, section, source, group, lookup))
        if len({item["stable_key"] for item in items}) != len(items):
            raise ValueError("Colisão de stable key nas Coleções Históricas.")
        if len({(item["section"], item["slug"]) for item in items}) != len(items):
            raise ValueError("Colisão de slug nas Coleções Históricas.")
        sections = []
        for order, section in enumerate(SOURCES, 1):
            rows = [item for item in items if item["section"] == section]
            title, description = SECTION_DATA[section]
            sections.append({"section": section, "title": title, "description": description, "display_order": order,
                             "items_count": len(rows), "ready": sum(x["status"] == "ready" for x in rows),
                             "review_required": sum(x["status"] == "review_required" for x in rows),
                             "unavailable": sum(x["status"] == "unavailable" for x in rows)})
        duration = int((time.perf_counter() - clock) * 1000)
        run = {"started_at": started, "completed_at": utc_now(), "status": "completed",
               "schema_version": COLLECTIONS_SCHEMA_VERSION, "total_items": len(items),
               "ready": sum(x["status"] == "ready" for x in items),
               "review_required": sum(x["status"] == "review_required" for x in items),
               "unavailable": sum(x["status"] == "unavailable" for x in items),
               "duration_ms": duration, "error_message": None}
        run_id = self.repository.persist(run, sections, items)
        return {"run": run_id, **run, "sections": sections}

    def status(self) -> dict:
        run = self.repository.latest_run()
        return {"available": run is not None, "schemaVersion": COLLECTIONS_SCHEMA_VERSION,
                "lastBuild": None if run is None else self.repository.summary()}
