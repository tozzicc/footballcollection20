from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from app.models.scanner import (
    ExtensionSummary,
    ScanError,
    ScannerCategories,
    ScannerFile,
    ScannerFolder,
    ScannerRequest,
    ScannerResponse,
)
from app.services.workspace_reader import WorkspaceReader
from app.services.workspace_service import validate_workspace_path

CATEGORY_EXTENSIONS: dict[str, tuple[str, ...]] = {
    "images": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tif", ".tiff"),
    "pages": (".htm", ".html", ".asp"),
    "data": (".json", ".xml", ".csv", ".dat"),
    "videos": (".mp4", ".avi", ".mov", ".mkv", ".webm", ".mpeg", ".mpg"),
    "audio": (".mp3", ".wav", ".flac", ".aac", ".ogg"),
    "documents": (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".rtf"),
    "archives": (".zip", ".rar", ".7z", ".tar", ".gz"),
}


def classify_extension(extension: str) -> str:
    normalized_extension = extension.lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if normalized_extension in extensions:
            return category
    return "other"


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def scan_workspace(raw_path: str) -> ScannerResponse:
    validation = validate_workspace_path(raw_path)
    if not validation.valid:
        raise ValueError(validation.message)

    workspace_path = Path(validation.normalizedPath)
    started_at = datetime.now(timezone.utc)
    reader = WorkspaceReader(str(workspace_path))
    categories = ScannerCategories()
    extension_counts: dict[str, int] = {}
    errors: list[ScanError] = []
    files: list[ScannerFile] = []
    folders: list[ScannerFolder] = []
    total_bytes = 0

    for entry in reader.iter_entries():
        if entry.metadata_error:
            errors.append(ScanError(path=str(entry.path), message=f"Não foi possível ler metadados: {entry.metadata_error}"))
        if entry.is_directory:
            relative = entry.relative_path
            folders.append(ScannerFolder(
                absolutePath=str(entry.path),
                relativePath=relative,
                name=entry.path.name,
                parent=None if relative == "." else (entry.path.parent.relative_to(workspace_path).as_posix() or "."),
                depth=0 if relative == "." else len(Path(relative).parts),
                readable=entry.readable,
            ))
            continue

        extension = entry.path.suffix.lower()
        category = classify_extension(extension)
        extension_counts[extension] = extension_counts.get(extension, 0) + 1
        setattr(categories, category, getattr(categories, category) + 1)
        total_bytes += entry.size
        files.append(ScannerFile(
            relativePath=entry.relative_path,
            absolutePath=str(entry.path),
            directory=entry.path.parent.relative_to(workspace_path).as_posix() or ".",
            filename=entry.path.name,
            extension=extension,
            category=category,
            size=entry.size,
            createdAt=entry.created_at,
            modifiedAt=entry.modified_at,
            readable=entry.readable,
        ))

    finished_at = datetime.now(timezone.utc)
    extensions = [
        ExtensionSummary(extension=extension, count=count)
        for extension, count in sorted(extension_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    return ScannerResponse(
        status="completed",
        workspacePath=str(workspace_path),
        startedAt=_format_timestamp(started_at),
        finishedAt=_format_timestamp(finished_at),
        durationMs=int((finished_at - started_at).total_seconds() * 1000),
        totalFiles=len(files),
        totalDirectories=len(folders),
        totalBytes=total_bytes,
        categories=categories,
        extensions=extensions,
        errors=errors,
        message="Análise concluída com sucesso.",
        files=files,
        folders=folders,
    )


def scan_workspace_request(request: ScannerRequest) -> ScannerResponse:
    return scan_workspace(request.workspacePath)