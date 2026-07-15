from pydantic import BaseModel, Field


class ScannerRequest(BaseModel):
    workspacePath: str


class ScannerCategories(BaseModel):
    images: int = 0
    pages: int = 0
    data: int = 0
    videos: int = 0
    audio: int = 0
    documents: int = 0
    archives: int = 0
    other: int = 0


class ExtensionSummary(BaseModel):
    extension: str
    count: int


class ScanError(BaseModel):
    path: str
    message: str


class ScannerFile(BaseModel):
    relativePath: str
    absolutePath: str
    directory: str
    filename: str
    extension: str
    category: str
    size: int
    createdAt: str | None = None
    modifiedAt: str | None = None
    readable: bool
    isDirectory: bool = False


class ScannerFolder(BaseModel):
    absolutePath: str
    relativePath: str
    name: str
    parent: str | None = None
    depth: int
    readable: bool
    isDirectory: bool = True


class ScannerResponse(BaseModel):
    status: str
    workspacePath: str
    startedAt: str
    finishedAt: str
    durationMs: int
    totalFiles: int
    totalDirectories: int
    totalBytes: int
    categories: ScannerCategories
    extensions: list[ExtensionSummary]
    errors: list[ScanError]
    message: str
    files: list[ScannerFile] = Field(default_factory=list)
    folders: list[ScannerFolder] = Field(default_factory=list)