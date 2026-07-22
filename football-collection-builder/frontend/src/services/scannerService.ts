import type { ScannerRequest, ScannerResponse } from '../types/scanner'
import { ApiClient } from './apiClient'

const apiClient = new ApiClient({ timeoutMs: 300000 })

export const scanWorkspace = async (workspacePath: string): Promise<ScannerResponse> => {
  const payload: ScannerRequest = { workspacePath }
  return apiClient.post<ScannerResponse>('/api/scanner/scan', payload)
}
