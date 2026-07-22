import type { Inventory, InventoryDatabaseStatus, InventoryPersistenceResult } from '../types/inventory'
import { ApiClient } from './apiClient'

const apiClient = new ApiClient({ timeoutMs: 300000 })

export const saveInventory = (inventory: Inventory): Promise<InventoryPersistenceResult> =>
  apiClient.post<InventoryPersistenceResult>('/api/inventory/save', inventory)

export const getInventoryDatabaseStatus = (): Promise<InventoryDatabaseStatus> =>
  apiClient.get<InventoryDatabaseStatus>('/api/inventory/status')