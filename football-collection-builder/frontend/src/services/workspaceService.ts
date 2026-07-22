import type { WorkspaceValidationResponse } from '../types/workspace'
import { ApiClient } from './apiClient'

const apiClient = new ApiClient()

export const validateWorkspace = async (
  workspacePath: string,
): Promise<WorkspaceValidationResponse> => {
  return apiClient.post<WorkspaceValidationResponse>('/api/workspace/validate', {
    workspacePath,
  })
}
