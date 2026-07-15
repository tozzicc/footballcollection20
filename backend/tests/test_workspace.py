import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_validate_workspace_valid_directory(client, tmp_path: Path):
    response = client.post(
        "/api/workspace/validate",
        json={"workspacePath": str(tmp_path)},
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["valid"] is True
    assert payload["exists"] is True
    assert payload["isDirectory"] is True
    assert payload["readable"] is True
    assert payload["normalizedPath"] == str(tmp_path.resolve())
    assert payload["message"] == "Workspace válido e acessível."


def test_validate_workspace_nonexistent_directory(client):
    path = "C:/path/does/not/exist"
    response = client.post(
        "/api/workspace/validate",
        json={"workspacePath": path},
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["valid"] is False
    assert payload["exists"] is False
    assert payload["isDirectory"] is False
    assert payload["readable"] is False
    assert payload["normalizedPath"] == os.path.normpath(path)
    assert payload["message"] == "O caminho informado não existe."


def test_validate_workspace_path_is_file(client, tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")

    response = client.post(
        "/api/workspace/validate",
        json={"workspacePath": str(test_file)},
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["valid"] is False
    assert payload["exists"] is True
    assert payload["isDirectory"] is False
    assert payload["readable"] is False
    assert payload["normalizedPath"] == str(test_file.resolve())
    assert payload["message"] == "O caminho informado não é uma pasta."


def test_validate_workspace_invalid_request(client):
    response = client.post("/api/workspace/validate", json={})

    assert response.status_code == 422
