import type { Workspace, WorkspaceInfo } from '../types/workspace'

export const workspaceMock: Workspace = {
  path: '',
  status: 'unconfigured',
}

export const workspaceInfoMock: WorkspaceInfo = {
  objective: 'O Workspace define a pasta raiz utilizada pelo Builder para localizar o acervo.',
  description: 'Este conteúdo é apenas ilustrativo.',
  exampleStructure: ['camisas/', 'memorabilia/', 'flags/', 'teams/', 'videos/'],
}
