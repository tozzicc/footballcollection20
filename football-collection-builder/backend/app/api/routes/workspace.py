from fastapi import APIRouter

from app.models.workspace import WorkspaceValidationRequest, WorkspaceValidationResponse
from app.services.workspace_service import validate_workspace_path

router = APIRouter()


@router.post("/workspace/validate", response_model=WorkspaceValidationResponse)
async def validate_workspace(request: WorkspaceValidationRequest):
    return validate_workspace_path(request.workspacePath)
