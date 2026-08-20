import sqlite3
from pathlib import Path

import pytest

from app.models.html_parser import HtmlParseRequest, HtmlReferenceStatus
from app.models.inventory import (
    Inventory, InventoryCategorySummary, InventoryExtensionSummary, InventoryItem,
    InventoryMetadata, InventoryStatistics,
)
from app.repositories.html_parser_repository import HtmlParserRepository
from app.repositories.inventory_repository import InventoryRepository
from app.services.html_parser_service import HtmlParserService


def item(root: Path, relative: str, identifier: str) -> InventoryItem:
    path = root / Path(relative)
    return InventoryItem(
        id=identifier, relativePath=relative.replace("\\", "/"), absolutePath=str(path),
        directory=str(Path(relative).parent), filename=path.name, extension=path.suffix,
        category="pages" if path.suffix.lower() in {".htm", ".html", ".asp"} else "images",
        size=path.stat().st_size if path.exists() else 0, readable=True,
    )


def service_for(root: Path, items: list[InventoryItem]) -> HtmlParserService:
    database = root / "builder.db"
    inventory_repository = InventoryRepository(database)
    pages = sum(x.category == "pages" for x in items)
    inventory_repository.save(Inventory(
        metadata=InventoryMetadata(generatedAt="2026-01-01T00:00:00Z", scannerVersion="test",
                                   workspacePath=str(root), durationMs=1),
        statistics=InventoryStatistics(
            totalFiles=len(items), totalDirectories=0, totalSize=sum(x.size for x in items),
            totalImages=len(items) - pages, totalPages=pages, totalVideos=0, totalDocuments=0,
            totalArchives=0, totalData=0, totalOther=0),
        folders=[], items=items,
        categories=[InventoryCategorySummary(category="pages", count=pages)],
        extensions=[InventoryExtensionSummary(extension=".html", count=pages)], errors=[]))
    return HtmlParserService(inventory_repository, HtmlParserRepository(database))


def details(service: HtmlParserService, search: str | None = None):
    page_id = service.repository.get_pages(50, 0, None, search).items[0].id
    return service.repository.get_page(page_id)


def test_metadata_headings_preview_title_and_malformed_html(tmp_path: Path):
    page = tmp_path / "index.html"
    page.write_text("""<html lang="pt-BR"><head><meta charset="utf-8"><title> Titulo </title>
      <meta name="description" content="Descricao"></head><body><!-- no --><style>hidden</style>
      <script>hidden()</script><h1>Cabecalho</h1><h2>Segundo</h2><p>Texto   visivel</p><div></body>""",
                    encoding="utf-8")
    service = service_for(tmp_path, [item(tmp_path, "index.html", "p")])
    result = service.parse(HtmlParseRequest(workspacePath=str(tmp_path)))
    value = details(service)
    assert result.parsedPages == 1 and value.title == "Titulo"
    assert value.metaDescription == "Descricao" and [x.level for x in value.headings] == [1, 2]
    assert "Texto visivel" in value.textPreview and "hidden" not in value.textPreview
    assert value.documentLanguage == "pt-BR" and value.charsetDeclared == "utf-8"


def test_title_fallback_static_asp_and_uppercase_extension(tmp_path: Path):
    page = tmp_path / "legacy.ASP"
    page.write_text("<% server_code %><html><body><h2>Fallback heading<div>", encoding="utf-8")
    service = service_for(tmp_path, [item(tmp_path, "legacy.ASP", "p")])
    service.parse(HtmlParseRequest(workspacePath=str(tmp_path)))
    assert details(service).title == "Fallback heading"


def test_images_and_links_classification_and_path_resolution(tmp_path: Path):
    (tmp_path / "pages").mkdir(); (tmp_path / "img").mkdir()
    page = tmp_path / "pages" / "index.html"
    target = tmp_path / "target.html"; image = tmp_path / "img" / "card one.jpg"
    target.write_text("<title>Target</title>", encoding="utf-8"); image.write_bytes(b"image")
    page.write_text("""<img src="../img/card%20one.jpg?x=1#part"><img src="missing.jpg">
      <img src="https://example.test/a.jpg"><img src="data:image/png;base64,AA">
      <a href="../target.html?x=1#part">Target</a><a href="missing.html">Missing</a>
      <a href="https://example.test">External</a><a href="#top">Anchor</a>
      <a href="mailto:a@b.test">Mail</a><a href="javascript:void(0)">JS</a>""", encoding="utf-8")
    service = service_for(tmp_path, [
        item(tmp_path, "pages/index.html", "p"), item(tmp_path, "target.html", "t"),
        item(tmp_path, "img/card one.jpg", "i")])
    service.parse(HtmlParseRequest(workspacePath=str(tmp_path)))
    value = details(service, "index")
    assert [x.status for x in value.imageReferences] == [
        HtmlReferenceStatus.RESOLVED, HtmlReferenceStatus.MISSING,
        HtmlReferenceStatus.EXTERNAL, HtmlReferenceStatus.IGNORED]
    assert [x.status for x in value.linkReferences] == [
        HtmlReferenceStatus.RESOLVED, HtmlReferenceStatus.MISSING, HtmlReferenceStatus.EXTERNAL,
        HtmlReferenceStatus.ANCHOR, HtmlReferenceStatus.IGNORED, HtmlReferenceStatus.IGNORED]
    assert value.imageReferences[0].referencedInventoryItemId == "i"


@pytest.mark.parametrize(("payload", "expected"), [
    (b"hello", "utf-8"), (b"preco \x80", "cp1252"),
    (b"invalid \x81", "latin-1"), (b"\xef\xbb\xbfhello", "utf-8-sig")])
def test_controlled_encoding_fallback(payload: bytes, expected: str):
    assert HtmlParserService._decode(payload)[1] == expected


def test_error_continuation_and_original_unchanged(tmp_path: Path):
    good = tmp_path / "good.html"; bad = tmp_path / "gone.html"
    good.write_text("<title>Good</title>", encoding="utf-8")
    before = good.read_bytes(), good.stat().st_mtime_ns
    missing = InventoryItem(id="bad", relativePath="gone.html", absolutePath=str(bad), directory=".",
                            filename="gone.html", extension=".html", category="pages", size=1, readable=True)
    service = service_for(tmp_path, [item(tmp_path, "good.html", "good"), missing])
    result = service.parse(HtmlParseRequest(workspacePath=str(tmp_path)))
    assert (result.parsedPages, result.failedPages) == (1, 1)
    assert (good.read_bytes(), good.stat().st_mtime_ns) == before and not bad.exists()


def test_persistence_replace_pagination_missing_and_rollback(tmp_path: Path, monkeypatch):
    page = tmp_path / "index.html"; page.write_text('<img src="none.jpg">', encoding="utf-8")
    service = service_for(tmp_path, [item(tmp_path, "index.html", "p")])
    first = service.parse(HtmlParseRequest(workspacePath=str(tmp_path)))
    assert service.repository.get_pages(1, 0, None, "index").total == 1
    assert service.repository.get_missing_references(1, 0, "image").total == 1
    second = service.parse(HtmlParseRequest(workspacePath=str(tmp_path), replacePrevious=True))
    assert second.runId != first.runId and service.repository.get_pages(50, 0, None, None).total == 1
    previous = service.repository.get_latest_run().id
    monkeypatch.setattr(service.repository, "_save_page",
                        lambda *args: (_ for _ in ()).throw(sqlite3.DatabaseError("forced")))
    with pytest.raises(sqlite3.DatabaseError):
        service.parse(HtmlParseRequest(workspacePath=str(tmp_path)))
    assert service.repository.get_latest_run().id == previous


def test_inventory_validation(tmp_path: Path):
    empty = HtmlParserService(InventoryRepository(tmp_path / "empty.db"), HtmlParserRepository(tmp_path / "empty.db"))
    with pytest.raises(ValueError, match="Inventory"):
        empty.parse(HtmlParseRequest(workspacePath=str(tmp_path)))
    page = tmp_path / "index.html"; page.write_text("ok", encoding="utf-8")
    service = service_for(tmp_path, [item(tmp_path, "index.html", "p")])
    with pytest.raises(ValueError, match="coincide"):
        service.parse(HtmlParseRequest(workspacePath=str(tmp_path / "other")))

def test_structural_image_contexts_are_conservative(tmp_path: Path):
    image1=tmp_path/'one.jpg';image2=tmp_path/'two.jpg';image1.write_bytes(b'x');image2.write_bytes(b'x')
    page=tmp_path/'index.html';page.write_text('''<table><tr><td><img src="one.jpg"></td><td><img src="two.jpg"></td></tr></table><table><tr><td>CAMISA HISTORICA - COPA</td></tr></table>''',encoding='utf-8')
    service=service_for(tmp_path,[item(tmp_path,'index.html','p'),item(tmp_path,'one.jpg','i1'),item(tmp_path,'two.jpg','i2')]);service.parse(HtmlParseRequest(workspacePath=str(tmp_path)));value=details(service)
    assert [x.status for x in value.imageContexts]==['matched','matched']
    assert all(x.contextText=='CAMISA HISTORICA - COPA' and x.extractionRule=='HX001' for x in value.imageContexts)
    assert len({x.structuralGroupKey for x in value.imageContexts})==1
    assert all(x.imageContainerDomIndex is not None and x.descriptionContainerDomIndex is not None for x in value.imageContexts)

def test_repeated_hx001_descriptions_keep_distinct_deterministic_groups(tmp_path: Path):
    for name in ('a.jpg','b.jpg','c.jpg','d.jpg'):(tmp_path/name).write_bytes(b'x')
    page=tmp_path/'index.html';page.write_text('''<table><img src="a.jpg"><img src="b.jpg"></table><table>MESMA DESCRICAO</table><table><img src="c.jpg"><img src="d.jpg"></table><table>MESMA DESCRICAO</table>''',encoding='utf-8')
    service=service_for(tmp_path,[item(tmp_path,'index.html','p'),*[item(tmp_path,f'{x}.jpg',x) for x in 'abcd']]);service.parse(HtmlParseRequest(workspacePath=str(tmp_path)));first=details(service).imageContexts
    service.parse(HtmlParseRequest(workspacePath=str(tmp_path)));second=details(service).imageContexts
    assert [x.structuralGroupKey for x in first]==[x.structuralGroupKey for x in second]
    assert first[0].structuralGroupKey==first[1].structuralGroupKey and first[2].structuralGroupKey==first[3].structuralGroupKey
    assert first[0].structuralGroupKey!=first[2].structuralGroupKey
    assert first[0].imageContainerDomIndex!=first[2].imageContainerDomIndex
    assert first[0].descriptionContainerDomIndex!=first[2].descriptionContainerDomIndex

@pytest.mark.parametrize(("markup", "rule", "container_type"), [
    ('<table><tr><td><img src="one.jpg">CAMISA NA CELULA</td></tr></table>', 'HX002', 'td'),
    ('<figure><img src="one.jpg"><figcaption>CAMISA NO BLOCO</figcaption></figure>', 'HX003', 'figure'),
])
def test_cell_and_block_contexts_persist_structural_identity(
    tmp_path: Path, markup: str, rule: str, container_type: str,
):
    (tmp_path/'one.jpg').write_bytes(b'x')
    page=tmp_path/'index.html';page.write_text(markup,encoding='utf-8')
    service=service_for(tmp_path,[item(tmp_path,'index.html','p'),item(tmp_path,'one.jpg','i1')])
    service.parse(HtmlParseRequest(workspacePath=str(tmp_path)));context=details(service).imageContexts[0]
    assert context.status=='matched' and context.extractionRule==rule
    assert context.structuralGroupKey and context.imageContainerType==container_type
    assert context.descriptionContainerType==container_type
    assert context.imageContainerDomIndex==context.descriptionContainerDomIndex

def test_ambiguous_and_missing_image_contexts(tmp_path: Path):
    for name in ('one.jpg','two.jpg'): (tmp_path/name).write_bytes(b'x')
    page=tmp_path/'index.html';page.write_text('<div><img src="one.jpg"><img src="two.jpg">texto compartilhado</div><img src="one.jpg">',encoding='utf-8')
    service=service_for(tmp_path,[item(tmp_path,'index.html','p'),item(tmp_path,'one.jpg','i1'),item(tmp_path,'two.jpg','i2')]);service.parse(HtmlParseRequest(workspacePath=str(tmp_path)));contexts=details(service).imageContexts
    assert contexts[0].status=='ambiguous' and contexts[1].status=='ambiguous'
    assert contexts[0].structuralGroupKey==contexts[1].structuralGroupKey
    assert contexts[2].status=='unsupported_structure' and contexts[2].contextText is None

