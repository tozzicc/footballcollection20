export type WorkspaceValidationResult = {
  valid: boolean
  message?: string
}

const MIN_WORKSPACE_LENGTH = 3

export const validateWorkspacePath = (value: string): WorkspaceValidationResult => {
  const trimmed = value.trim()

  if (!trimmed) {
    return {
      valid: false,
      message: 'Campo obrigatório. Informe o caminho do acervo.',
    }
  }

  if (trimmed.length < MIN_WORKSPACE_LENGTH) {
    return {
      valid: false,
      message: 'O caminho é muito curto. Informe um caminho com pelo menos 3 caracteres.',
    }
  }

  const repeatedSlashes = /[\\/]{2,}/
  if (repeatedSlashes.test(trimmed)) {
    return {
      valid: false,
      message: 'O caminho não pode conter barras duplicadas.',
    }
  }

  return { valid: true }
}
