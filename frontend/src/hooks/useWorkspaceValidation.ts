import { useCallback, useState } from 'react'

import { validateWorkspace } from '../services/workspaceService'
import type { WorkspaceValidationResponse } from '../types/workspace'

export type WorkspaceValidationState = {
  validationResult: WorkspaceValidationResponse | null
  isValidating: boolean
  validationError: string
  lastValidatedAt: string | null
}

const useWorkspaceValidation = () => {
  const [validationResult, setValidationResult] = useState<WorkspaceValidationResponse | null>(null)
  const [isValidating, setIsValidating] = useState(false)
  const [validationError, setValidationError] = useState('')
  const [lastValidatedAt, setLastValidatedAt] = useState<string | null>(null)

  const validateWorkspacePath = useCallback(async (path: string) => {
    setIsValidating(true)
    setValidationError('')

    try {
      const result = await validateWorkspace(path)
      setValidationResult(result)
      setLastValidatedAt(new Date().toISOString())
      return result
    } catch (error) {
      const message = error instanceof Error
        ? error.message
        : 'Não foi possível conectar ao serviço do Builder. Verifique se o backend está em execução.'
      setValidationError(message)
      setValidationResult(null)
      return null
    } finally {
      setIsValidating(false)
    }
  }, [])

  const resetValidation = useCallback(() => {
    setValidationResult(null)
    setValidationError('')
    setLastValidatedAt(null)
    setIsValidating(false)
  }, [])

  return {
    validateWorkspace: validateWorkspacePath,
    validationResult,
    isValidating,
    validationError,
    lastValidatedAt,
    resetValidation,
  }
}

export default useWorkspaceValidation
