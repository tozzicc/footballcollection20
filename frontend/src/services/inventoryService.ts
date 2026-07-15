import type { Inventory, InventoryRequest } from '../types/inventory'
import { ApiClient } from './apiClient'

const apiClient = new ApiClient({ timeoutMs: 300000 })

export const buildInventory = (workspacePath: string): Promise<Inventory> => {
  const payload: InventoryRequest = { workspacePath }
  return apiClient.post<Inventory>('/api/inventory/build', payload)
}