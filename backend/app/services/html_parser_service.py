from __future__ import annotations

import codecs
import os
import posixpath
import re
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

from app.models.html_parser import (
    HtmlHeading, HtmlImageReference, HtmlLinkReference, HtmlPageResult, HtmlParseError,
    HtmlParseRequest, HtmlParseResponse, HtmlParseRun, HtmlParseStatus, HtmlParserStatus,
    HtmlReferenceStatus,
)
from app.models.inventory import InventoryItem
from app.repositories.html_parser_repository import HtmlParserRepository
from app.repositories.inventory_repository import InventoryRepository


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class HtmlParserService:
    def __init__(
        self, inventory_repository: InventoryRepository | None = None,
        parser_repository: HtmlParserRepository | None = None,
    ):
        self.inventory_repository = inventory_repository or InventoryRepository()
        self.repository = parser_repository or HtmlParserRepository()

    def status(self) -> HtmlParserStatus:
        workspace = self.inventory_repository.get_workspace_path()
        pages = self.inventory_repository.get_html_pages() if workspace else []
        latest = self.repository.get_latest_run()
        return HtmlParserStatus(
            hasRun=latest is not None, inventoryAvailable=workspace is not None,
            availablePages=len(pages), lastRun=latest,
        )

    def parse(self, request: HtmlParseRequest) -> HtmlParseResponse:
        saved_workspace = self.inventory_repository.get_workspace_path()
        if saved_workspace is None:
            raise ValueError("Nenhum Inventory salvo. Construa e salve o Inventory antes do parser.")
        if os.path.normcase(os.path.abspath(saved_workspace)) != os.path.normcase(os.path.abspath(request.workspacePath)):
            raise ValueError("workspacePath nao coincide com o Inventory persistido.")
        items = self.inventory_repository.get_html_pages()
        inventory = self.inventory_repository.get_inventory()
        if inventory is None:
            raise ValueError("Inventory persistido indisponivel.")
        lookup = {self._key(x.relativePath): x for x in inventory.items if not x.isDirectory}
        started_at, timer = _utc_now(), perf_counter()
        pages: list[HtmlPageResult] = []
        errors: list[HtmlParseError] = []
        for item in items:
            try:
                pages.append(self.parse_page(item, Path(saved_workspace), lookup))
            except Exception as exc:
                message = str(exc) or exc.__class__.__name__
                errors.append(HtmlParseError(
                    inventoryItemId=item.id, relativePath=item.relativePath,
                    errorType=exc.__class__.__name__, message=message,
                ))
                pages.append(HtmlPageResult(
                    inventoryItemId=item.id, relativePath=item.relativePath,
                    absolutePath=item.absolutePath, filename=item.filename, extension=item.extension,
                    fileSize=item.size, createdAt=item.createdAt, modifiedAt=item.modifiedAt,
                    title=Path(item.filename).stem, parseStatus="failed", parseMessage=message,
                ))
        failed = len(errors)
        images = sum(len(x.imageReferences) for x in pages)
        internal = sum(1 for p in pages for x in p.linkReferences if not x.isExternal and x.status == HtmlReferenceStatus.RESOLVED)
        external = sum(1 for p in pages for x in p.linkReferences if x.isExternal)
        missing = sum(1 for p in pages for x in [*p.imageReferences, *p.linkReferences]
                      if x.status == HtmlReferenceStatus.MISSING)
        run = HtmlParseRun(
            workspacePath=saved_workspace, startedAt=started_at, finishedAt=_utc_now(),
            durationMs=round((perf_counter() - timer) * 1000),
            status=HtmlParseStatus.COMPLETED_WITH_ERRORS if failed else HtmlParseStatus.COMPLETED,
            totalPages=len(items), parsedPages=len(items) - failed, failedPages=failed,
            imageReferences=images, internalLinks=internal, externalLinks=external,
            missingReferences=missing,
            message="Parser HTML concluido com falhas." if failed else "Parser HTML concluido.",
        )
        run_id = self.repository.save_run(run, pages, errors, request.replacePrevious)
        return HtmlParseResponse(**run.model_dump(), runId=run_id, errors=errors)

    def parse_page(
        self, item: InventoryItem, workspace: Path, lookup: dict[str, InventoryItem],
    ) -> HtmlPageResult:
        path = Path(item.absolutePath)
        workspace_resolved = workspace.resolve()
        try:
            path.resolve().relative_to(workspace_resolved)
        except ValueError as exc:
            raise ValueError("Arquivo do Inventory esta fora do Workspace.") from exc
        raw = path.read_bytes()
        text, encoding = self._decode(raw)
        soup = BeautifulSoup(text, "html.parser")
        declared = self._declared_charset(raw)
        headings = [
            HtmlHeading(level=int(tag.name[1]), position=index, text=self._clean(tag.get_text(" ", strip=True)))
            for index, tag in enumerate(soup.find_all(["h1", "h2", "h3"]))
            if self._clean(tag.get_text(" ", strip=True))
        ]
        title_tag = soup.find("title")
        candidates = [
            self._clean(title_tag.get_text(" ", strip=True)) if title_tag else "",
            next((h.text for h in headings if h.level == 1), ""),
            headings[0].text if headings else "",
            Path(item.filename).stem,
        ]
        for removable in soup(["script", "style"]):
            removable.decompose()
        description = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        html_tag = soup.find("html")
        images = [self._image(tag, item.relativePath, workspace, lookup) for tag in soup.find_all("img")]
        links = [self._link(tag, item.relativePath, lookup) for tag in soup.find_all("a") if tag.has_attr("href")]
        return HtmlPageResult(
            inventoryItemId=item.id, relativePath=item.relativePath, absolutePath=item.absolutePath,
            filename=item.filename, extension=item.extension, fileSize=item.size,
            createdAt=item.createdAt, modifiedAt=item.modifiedAt, encodingUsed=encoding,
            title=next(value for value in candidates if value),
            documentLanguage=html_tag.get("lang") if html_tag else None,
            charsetDeclared=declared,
            metaDescription=self._clean(str(description.get("content", ""))) or None if description else None,
            headings=headings, textPreview=self._clean(soup.get_text(" ", strip=True))[:500],
            imageReferences=images, linkReferences=links,
            parseStatus="parsed", parseMessage="Pagina analisada com sucesso.",
        )

    @staticmethod
    def _decode(raw: bytes) -> tuple[str, str]:
        if raw.startswith(codecs.BOM_UTF8):
            return raw.decode("utf-8-sig"), "utf-8-sig"
        if raw.startswith(codecs.BOM_UTF16_LE):
            return raw.decode("utf-16"), "utf-16"
        if raw.startswith(codecs.BOM_UTF16_BE):
            return raw.decode("utf-16"), "utf-16"
        declared = HtmlParserService._declared_charset(raw)
        candidates = [declared, "utf-8", "cp1252", "latin-1"]
        for encoding in dict.fromkeys(x for x in candidates if x):
            try:
                return raw.decode(encoding), encoding.lower()
            except (UnicodeDecodeError, LookupError):
                continue
        return raw.decode("latin-1"), "latin-1"

    @staticmethod
    def _declared_charset(raw: bytes) -> str | None:
        head = raw[:8192].decode("latin-1", errors="ignore")
        match = re.search(r"charset\s*=\s*['\"]?\s*([a-zA-Z0-9._-]+)", head, re.I)
        return match.group(1).lower() if match else None

    @staticmethod
    def _clean(value: str) -> str:
        return re.sub(r"\s+", " ", value).strip()

    @staticmethod
    def _key(path: str) -> str:
        normalized = posixpath.normpath(unquote(path).replace("\\", "/").lstrip("/"))
        return normalized.casefold() if os.name == "nt" else normalized

    def _resolve(self, value: str, source: str, lookup: dict[str, InventoryItem]) -> tuple[str, InventoryItem | None]:
        split = urlsplit(value.replace("\\", "/"))
        decoded = unquote(split.path)
        if decoded.startswith("/"):
            relative = posixpath.normpath(decoded.lstrip("/"))
        else:
            relative = posixpath.normpath(posixpath.join(posixpath.dirname(source.replace("\\", "/")), decoded))
        return relative, lookup.get(self._key(relative))

    def _image(self, tag, source: str, workspace: Path, lookup: dict[str, InventoryItem]) -> HtmlImageReference:
        original = str(tag.get("src", "")).strip()
        normalized = unquote(original.replace("\\", "/"))
        lower = original.lower()
        external = lower.startswith(("http://", "https://", "//"))
        if external:
            status, relative, found = HtmlReferenceStatus.EXTERNAL, None, None
        elif lower.startswith("data:"):
            status, relative, found = HtmlReferenceStatus.IGNORED, None, None
        elif not original:
            status, relative, found = HtmlReferenceStatus.INVALID, None, None
        else:
            relative, found = self._resolve(original, source, lookup)
            status = HtmlReferenceStatus.RESOLVED if found else HtmlReferenceStatus.MISSING
        return HtmlImageReference(
            srcOriginal=original, srcNormalized=normalized, alt=tag.get("alt"), title=tag.get("title"),
            widthDeclared=tag.get("width"), heightDeclared=tag.get("height"), isExternal=external,
            resolvedRelativePath=relative,
            resolvedAbsolutePath=str(workspace / Path(relative)) if relative else None,
            existsInInventory=found is not None,
            referencedInventoryItemId=found.id if found else None, status=status,
        )

    def _link(self, tag, source: str, lookup: dict[str, InventoryItem]) -> HtmlLinkReference:
        original = str(tag.get("href", "")).strip()
        normalized, lower = unquote(original.replace("\\", "/")), original.lower()
        external = lower.startswith(("http://", "https://", "//"))
        anchor, mailto, javascript = lower.startswith("#"), lower.startswith("mailto:"), lower.startswith("javascript:")
        relative = None
        found = None
        if external:
            status = HtmlReferenceStatus.EXTERNAL
        elif anchor:
            status = HtmlReferenceStatus.ANCHOR
        elif mailto or javascript:
            status = HtmlReferenceStatus.IGNORED
        elif not original:
            status = HtmlReferenceStatus.INVALID
        else:
            relative, found = self._resolve(original, source, lookup)
            status = HtmlReferenceStatus.RESOLVED if found else HtmlReferenceStatus.MISSING
        return HtmlLinkReference(
            hrefOriginal=original, hrefNormalized=normalized,
            visibleText=self._clean(tag.get_text(" ", strip=True)) or None, title=tag.get("title"),
            isExternal=external, isAnchor=anchor, isMailto=mailto, isJavascript=javascript,
            resolvedRelativePath=relative, existsInInventory=found is not None,
            referencedInventoryItemId=found.id if found else None, status=status,
        )
