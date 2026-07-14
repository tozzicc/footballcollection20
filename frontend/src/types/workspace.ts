export type WorkspaceStatus = 'unconfigured' | 'configured'

export type Workspace = {
  path: string
  status: WorkspaceStatus
}

export type WorkspaceStorageEntry = {
  workspacePath: string
  savedAt: string
  version: number
  status: WorkspaceStatus
}

export type WorkspaceInfo = {
  objective: string
  description: string
  exampleStructure: string[]
}
