from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.models.scanner import (
    ExtensionSummary,
    ScannerCategories,
    ScannerFile,
    ScannerFolder,
    ScannerResponse,
)
from app.services.inventory_builder import build_inventory
from app.services.inventory_service import InventoryService


def scanner_response(files=None, folders=None, categories=None, extensions=None):
    files = files or []
    folders = folders or []
    return ScannerResponse(
        status="completed",
        workspacePath="C:/collection",
        startedAt="2026-01-01T00:00:00Z",
        finishedAt="2026-01-01T00:00:01Z",
        durationMs=1000,
        totalFiles=len(files),
        totalDirectories=len(folders),
        totalBytes=sum(item.size for item in files),
        categories=categories or ScannerCategories(),
        extensions=extensions or [],
        errors=[],
        message="Análise concluída com sucesso.",
        files=files,
        folders=folders,
    )


def test_build_empty_inventory():
    inventory = build_inventory(scanner_response())
    assert inventory.statistics.totalFiles == 0
    assert inventory.statistics.totalDirectories == 0
    assert inventory.statistics.totalSize == 0
    assert inventory.items == []
    assert inventory.folders == []


def test_build_inventory_with_files_and_statistics():
    files = [
        ScannerFile(relativePath="images/a.jpg", absolutePath="C:/collection/images/a.jpg", directory="images", filename="a.jpg", extension=".jpg", category="images", size=12, createdAt="2026-01-01T00:00:00Z", modifiedAt="2026-01-02T00:00:00Z", readable=True),
        ScannerFile(relativePath="index.html", absolutePath="C:/collection/index.html", directory=".", filename="index.html", extension=".html", category="pages", size=8, readable=True),
    ]
    scan = scanner_response(
        files=files,
        categories=ScannerCategories(images=1, pages=1),
        extensions=[ExtensionSummary(extension=".html", count=1), ExtensionSummary(extension=".jpg", count=1)],
    )
    inventory = build_inventory(scan)
    assert len(inventory.items) == 2
    assert inventory.statistics.totalFiles == 2
    assert inventory.statistics.totalSize == 20
    assert inventory.statistics.totalImages == 1
    assert inventory.statistics.totalPages == 1
    assert inventory.items[0].id
    assert inventory.items[0].createdAt == "2026-01-01T00:00:00Z"


def test_build_inventory_with_folders():
    folders = [
        ScannerFolder(absolutePath="C:/collection", relativePath=".", name="collection", parent=None, depth=0, readable=True),
        ScannerFolder(absolutePath="C:/collection/images", relativePath="images", name="images", parent=".", depth=1, readable=True),
    ]
    inventory = build_inventory(scanner_response(folders=folders))
    assert inventory.statistics.totalDirectories == 2
    assert inventory.folders[1].parent == "."
    assert inventory.folders[1].depth == 1


def test_build_inventory_with_multiple_extensions():
    scan = scanner_response(extensions=[ExtensionSummary(extension=".jpg", count=3), ExtensionSummary(extension=".png", count=2)])
    inventory = build_inventory(scan)
    assert [(item.extension, item.count) for item in inventory.extensions] == [(".jpg", 3), (".png", 2)]


def test_build_inventory_with_categories():
    scan = scanner_response(categories=ScannerCategories(images=2, videos=1, audio=1, other=3))
    inventory = build_inventory(scan)
    summaries = {item.category: item.count for item in inventory.categories}
    assert summaries["images"] == 2
    assert summaries["videos"] == 1
    assert summaries["audio"] == 1
    assert inventory.statistics.totalOther == 3


def test_inventory_builder_does_not_access_filesystem(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Inventory Builder não pode acessar o disco")

    monkeypatch.setattr(Path, "rglob", forbidden)
    monkeypatch.setattr(Path, "stat", forbidden)
    inventory = build_inventory(scanner_response())
    assert inventory.statistics.totalFiles == 0


def test_inventory_service_validates_consistency():
    inventory = build_inventory(scanner_response())
    assert InventoryService().validate(inventory) is True


def test_inventory_endpoint_builds_from_workspace(tmp_path: Path):
    (tmp_path / "album.jpg").write_bytes(b"card")
    response = TestClient(app).post("/api/inventory/build", json={"workspacePath": str(tmp_path)})
    assert response.status_code == 200
    payload = response.json()
    assert payload["statistics"]["totalFiles"] == 1
    assert payload["items"][0]["filename"] == "album.jpg"