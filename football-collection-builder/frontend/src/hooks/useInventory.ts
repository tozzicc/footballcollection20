import { useCallback, useState } from 'react'
import { buildInventory } from '../services/inventoryService'
import type { Inventory } from '../types/inventory'

export type InventoryStatus = 'idle' | 'building' | 'completed' | 'error'

const useInventory = () => {
  const [inventory, setInventory] = useState<Inventory | null>(null)
  const [status, setStatus] = useState<InventoryStatus>('idle')
  const [error, setError] = useState('')

  const build = useCallback(async (workspacePath: string) => {
    setStatus('building')
    setError('')
    try {
      setInventory(await buildInventory(workspacePath))
      setStatus('completed')
    } catch (caught) {
      setInventory(null)
      setError(caught instanceof Error ? caught.message : 'Falha inesperada ao construir o Inventory.')
      setStatus('error')
    }
  }, [])

  return { inventory, status, error, isBuilding: status === 'building', build }
}

export default useInventory