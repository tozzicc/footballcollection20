from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class WorkspaceValidationRequest(BaseModel):
    workspacePath: str


class WorkspaceValidationResponse(BaseModel):
    valid: bool
    exists: bool
    isDirectory: bool
    readable: bool
    normalizedPath: str
    message: str
