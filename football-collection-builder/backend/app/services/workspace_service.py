import os
from pathlib import Path

from app.models.workspace import WorkspaceValidationResponse


def normalize_workspace_path(raw_path: str) -> str:
    cleaned_path = raw_path.strip()
    if not cleaned_path:
        return ''

    expanded = os.path.expandvars(os.path.expanduser(cleaned_path))
    normalized_path = os.path.normpath(expanded)

    try:
        return str(Path(normalized_path).resolve(strict=False))
    except Exception:
        return normalized_path


def validate_workspace_path(raw_path: str) -> WorkspaceValidationResponse:
    normalized_path = normalize_workspace_path(raw_path)

    if not normalized_path:
        return WorkspaceValidationResponse(
            valid=False,
            exists=False,
            isDirectory=False,
            readable=False,
            normalizedPath="",
            message="Caminho vazio. Informe o caminho do Workspace.",
        )

    exists = os.path.exists(normalized_path)
    is_directory = os.path.isdir(normalized_path)
    readable = False

    if exists and is_directory:
        readable = os.access(normalized_path, os.R_OK)

    if not exists:
        return WorkspaceValidationResponse(
            valid=False,
            exists=False,
            isDirectory=False,
            readable=False,
            normalizedPath=normalized_path,
            message="O caminho informado não existe.",
        )

    if not is_directory:
        return WorkspaceValidationResponse(
            valid=False,
            exists=True,
            isDirectory=False,
            readable=False,
            normalizedPath=normalized_path,
            message="O caminho informado não é uma pasta.",
        )

    if not readable:
        return WorkspaceValidationResponse(
            valid=False,
            exists=True,
            isDirectory=True,
            readable=False,
            normalizedPath=normalized_path,
            message="Não há permissão de leitura para o caminho informado.",
        )

    return WorkspaceValidationResponse(
        valid=True,
        exists=True,
        isDirectory=True,
        readable=True,
        normalizedPath=normalized_path,
        message="Workspace válido e acessível.",
    )
