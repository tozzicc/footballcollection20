import { useCallback, useEffect, useState } from 'react'
import { getInventoryDatabaseStatus, saveInventory } from '../services/inventoryRepositoryService'
import type { Inventory, InventoryDatabaseStatus, InventoryPersistenceResult } from '../types/inventory'

const emptyStatus: InventoryDatabaseStatus = { databaseCreated: false, lastSavedAt: null, fileCount: 0, folderCount: 0 }

const useInventoryRepository = () => {
  const [databaseStatus, setDatabaseStatus] = useState<InventoryDatabaseStatus>(emptyStatus)
  const [saveResult, setSaveResult] = useState<InventoryPersistenceResult | null>(null)
  const [isSaving, setIsSaving] = useState(false)
  const [repositoryError, setRepositoryError] = useState('')

  const refreshStatus = useCallback(async () => {
    try {
      setDatabaseStatus(await getInventoryDatabaseStatus())
    } catch (caught) {
      setRepositoryError(caught instanceof Error ? caught.message : 'Falha ao consultar o banco.')
    }
  }, [])

  useEffect(() => {
    let active = true
    getInventoryDatabaseStatus()
      .then((status) => { if (active) setDatabaseStatus(status) })
      .catch((caught: unknown) => {
        if (active) setRepositoryError(caught instanceof Error ? caught.message : 'Falha ao consultar o banco.')
      })
    return () => { active = false }
  }, [])

  const save = useCallback(async (inventory: Inventory) => {
    setIsSaving(true)
    setRepositoryError('')
    try {
      const result = await saveInventory(inventory)
      setSaveResult(result)
      await refreshStatus()
    } catch (caught) {
      setSaveResult(null)
      setRepositoryError(caught instanceof Error ? caught.message : 'Falha ao salvar o Inventory.')
    } finally {
      setIsSaving(false)
    }
  }, [refreshStatus])

  return { databaseStatus, saveResult, isSaving, repositoryError, save, refreshStatus }
}

export default useInventoryRepository