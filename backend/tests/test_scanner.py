from pathlib import Path

import pytest

from app.services.scanner_service import scan_workspace


def test_scan_empty_directory(tmp_path: Path):
    response = scan_workspace(str(tmp_path))

    assert response.status == "completed"
    assert response.totalFiles == 0
    assert response.totalDirectories == 1
    assert response.totalBytes == 0
    assert response.categories.images == 0
    assert response.categories.pages == 0
    assert response.categories.other == 0
    assert response.errors == []


def test_scan_directory_with_subfolders(tmp_path: Path):
    nested = tmp_path / "nested"
    nested.mkdir()
    (tmp_path / "image.jpg").write_bytes(b"abc")
    (nested / "page.html").write_text("<html></html>")
    (nested / "notes.txt").write_text("notes")

    response = scan_workspace(str(tmp_path))

    assert response.totalFiles == 3
    assert response.totalDirectories == 2
    assert response.categories.images == 1
    assert response.categories.pages == 1
    assert response.categories.documents == 1
    assert response.categories.other == 0


def test_scan_counts_bytes_and_extensions(tmp_path: Path):
    (tmp_path / "a.jpg").write_bytes(b"1234")
    (tmp_path / "b.png").write_bytes(b"12")
    (tmp_path / "c").write_text("raw")

    response = scan_workspace(str(tmp_path))

    assert response.totalFiles == 3
    assert response.totalBytes == 4 + 2 + 3
    assert any(item.extension == ".jpg" and item.count == 1 for item in response.extensions)
    assert any(item.extension == ".png" and item.count == 1 for item in response.extensions)
    assert any(item.extension == "" and item.count == 1 for item in response.extensions)


def test_scan_classifies_uppercase_extensions(tmp_path: Path):
    (tmp_path / "photo.JPG").write_bytes(b"123")
    (tmp_path / "index.HTML").write_text("<body></body>")

    response = scan_workspace(str(tmp_path))

    assert response.categories.images == 1
    assert response.categories.pages == 1
    assert any(item.extension == ".jpg" for item in response.extensions)
    assert any(item.extension == ".html" for item in response.extensions)


def test_scan_classifies_files_without_extension_as_other(tmp_path: Path):
    (tmp_path / "README").write_text("docs")

    response = scan_workspace(str(tmp_path))

    assert response.categories.other == 1
    assert any(item.extension == "" for item in response.extensions)


def test_scan_rejects_nonexistent_path(tmp_path: Path):
    missing_path = tmp_path / "missing"

    with pytest.raises(ValueError, match="não existe"):
        scan_workspace(str(missing_path))


def test_scan_rejects_file_path(tmp_path: Path):
    file_path = tmp_path / "not-a-directory.txt"
    file_path.write_text("content")

    with pytest.raises(ValueError, match="não é uma pasta"):
        scan_workspace(str(file_path))


def test_scan_orders_extensions_by_count_desc(tmp_path: Path):
    (tmp_path / "one.jpg").write_bytes(b"1")
    (tmp_path / "two.jpg").write_bytes(b"1")
    (tmp_path / "three.png").write_bytes(b"1")

    response = scan_workspace(str(tmp_path))

    ordered_extensions = [item.extension for item in response.extensions]

    assert ordered_extensions[:2] == [".jpg", ".png"]
    assert response.extensions[0].count == 2
    assert response.extensions[1].count == 1


def test_scan_includes_started_and_finished_timestamps(tmp_path: Path):
    response = scan_workspace(str(tmp_path))

    assert response.startedAt
    assert response.finishedAt
    assert response.durationMs >= 0


def test_scan_response_keeps_legacy_fields(tmp_path: Path):
    response = scan_workspace(str(tmp_path)).model_dump()
    legacy_fields = {"status", "workspacePath", "startedAt", "finishedAt", "durationMs", "totalFiles", "totalDirectories", "totalBytes", "categories", "extensions", "errors", "message"}
    assert legacy_fields.issubset(response.keys())


def test_scan_generates_typed_file_and_folder_lists(tmp_path: Path):
    folder = tmp_path / "Cards"
    folder.mkdir()
    file_path = folder / "PLAYER.JPG"
    file_path.write_bytes(b"12345")
    response = scan_workspace(str(tmp_path))
    assert len(response.files) == 1
    assert len(response.folders) == 2
    file = response.files[0]
    assert file.relativePath == "Cards/PLAYER.JPG"
    assert file.absolutePath == str(file_path)
    assert file.directory == "Cards"
    assert file.filename == "PLAYER.JPG"
    assert file.extension == ".jpg"
    assert file.category == "images"
    assert file.size == 5
    assert file.createdAt
    assert file.modifiedAt
    assert file.isDirectory is False
    assert response.folders[0].relativePath == "."
    assert response.folders[1].depth == 1
    assert response.folders[1].isDirectory is True
