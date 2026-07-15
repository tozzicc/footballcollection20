from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class WorkspaceEntry:
    path: Path
    relative_path: str
    is_directory: bool
    readable: bool
    size: int
    created_at: str | None
    modified_at: str | None
    metadata_error: str | None = None


class WorkspaceReader:
    """Read-only access helper that collects metadata in one recursive pass."""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)

    @staticmethod
    def _format_timestamp(timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def _read_entry(self, item: Path) -> WorkspaceEntry:
        is_directory = item.is_dir()
        readable = os.access(item, os.R_OK)
        try:
            metadata = item.stat()
            return WorkspaceEntry(
                path=item,
                relative_path="." if item == self.workspace_path else item.relative_to(self.workspace_path).as_posix(),
                is_directory=is_directory,
                readable=readable,
                size=0 if is_directory else metadata.st_size,
                created_at=self._format_timestamp(metadata.st_ctime),
                modified_at=self._format_timestamp(metadata.st_mtime),
            )
        except OSError as exc:
            return WorkspaceEntry(
                path=item,
                relative_path="." if item == self.workspace_path else item.relative_to(self.workspace_path).as_posix(),
                is_directory=is_directory,
                readable=readable,
                size=0,
                created_at=None,
                modified_at=None,
                metadata_error=str(exc),
            )

    def iter_entries(self) -> Iterator[WorkspaceEntry]:
        """Yield the root and its descendants without following directory symlinks."""
        if not self.workspace_path.exists():
            raise FileNotFoundError("O caminho informado não existe.")
        if not self.workspace_path.is_dir():
            raise NotADirectoryError("O caminho informado não é uma pasta.")
        if not os.access(self.workspace_path, os.R_OK):
            raise PermissionError("Não há permissão de leitura para o caminho informado.")

        yield self._read_entry(self.workspace_path)
        for item in self.workspace_path.rglob("*"):
            if item.is_symlink() and item.is_dir():
                continue
            try:
                if item.is_dir() or item.is_file():
                    yield self._read_entry(item)
            except OSError:
                yield self._read_entry(item)

    def iter_items(self) -> Iterator[Path]:
        """Backward-compatible path iterator."""
        for entry in self.iter_entries():
            if entry.path != self.workspace_path:
                yield entry.path