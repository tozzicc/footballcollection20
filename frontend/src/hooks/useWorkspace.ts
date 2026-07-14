import { useState } from 'react'
import type { Workspace, WorkspaceStorageEntry } from '../types/workspace'
import { WORKSPACE_STORAGE_KEY } from '../constants/storageKeys'
import { loadStorageItem, removeStorageItem, saveStorageItem } from '../utils/storage'
import { validateWorkspacePath } from '../utils/workspaceValidation'

export type WorkspaceSaveStatus = 'success' | 'error' | ''

const DEFAULT_WORKSPACE: Workspace = {
  path: '',
  status: 'unconfigured',
}

const loadInitialWorkspace = (): {
  workspacePath: string
  workspace: Workspace
  isConfigured: boolean
  lastUpdated: string
} => {
  const saved = loadStorageItem<WorkspaceStorageEntry>(WORKSPACE_STORAGE_KEY)

  if (!saved || !saved.workspacePath) {
    return {
      workspacePath: '',
      workspace: DEFAULT_WORKSPACE,
      isConfigured: false,
      lastUpdated: '',
    }
  }

  return {
    workspacePath: saved.workspacePath,
    workspace: { path: saved.workspacePath, status: saved.status },
    isConfigured: saved.status === 'configured',
    lastUpdated: saved.savedAt,
  }
}

const useWorkspace = () => {
  const initialWorkspace = loadInitialWorkspace()

  const [workspacePath, setWorkspacePath] = useState(initialWorkspace.workspacePath)
  const [workspace, setWorkspace] = useState<Workspace>(initialWorkspace.workspace)
  const [isConfigured, setIsConfigured] = useState(initialWorkspace.isConfigured)
  const [lastUpdated, setLastUpdated] = useState(initialWorkspace.lastUpdated)
  const [feedbackMessage, setFeedbackMessage] = useState('')
  const [feedbackType, setFeedbackType] = useState<WorkspaceSaveStatus>('')

  const resetWorkspaceState = () => {
    setWorkspacePath('')
    setWorkspace(DEFAULT_WORKSPACE)
    setIsConfigured(false)
    setLastUpdated('')
    setFeedbackMessage('')
    setFeedbackType('')
  }

  const loadWorkspace = () => {
    const saved = loadStorageItem<WorkspaceStorageEntry>(WORKSPACE_STORAGE_KEY)

    if (!saved || !saved.workspacePath) {
      resetWorkspaceState()
      return
    }

    setWorkspacePath(saved.workspacePath)
    setWorkspace({ path: saved.workspacePath, status: saved.status })
    setIsConfigured(saved.status === 'configured')
    setLastUpdated(saved.savedAt)
    setFeedbackMessage('')
    setFeedbackType('')
  }

  const saveWorkspace = () => {
    const trimmedPath = workspacePath.trim()
    const validation = validateWorkspacePath(trimmedPath)

    if (!validation.valid) {
      setFeedbackMessage(validation.message ?? 'Caminho inválido.')
      setFeedbackType('error')
      setWorkspace({ path: trimmedPath, status: 'unconfigured' })
      setIsConfigured(false)
      return false
    }

    const savedAt = new Date().toISOString()
    const storageEntry: WorkspaceStorageEntry = {
      workspacePath: trimmedPath,
      savedAt,
      version: 1,
      status: 'configured',
    }

    saveStorageItem(WORKSPACE_STORAGE_KEY, storageEntry)
    setWorkspacePath(trimmedPath)
    setWorkspace({ path: trimmedPath, status: 'configured' })
    setIsConfigured(true)
    setLastUpdated(savedAt)
    setFeedbackMessage('Workspace salvo com sucesso.')
    setFeedbackType('success')
    return true
  }

  const clearWorkspace = () => {
    removeStorageItem(WORKSPACE_STORAGE_KEY)
    resetWorkspaceState()
    setFeedbackMessage('Workspace limpo.')
    setFeedbackType('success')
  }

  return {
    workspace,
    workspacePath,
    status: workspace.status,
    isConfigured,
    lastUpdated,
    feedbackMessage,
    feedbackType,
    setWorkspacePath,
    saveWorkspace,
    clearWorkspace,
    loadWorkspace,
  }
}

export default useWorkspace
