export type ScannerStatus = 'idle' | 'scanning' | 'completed' | 'error'

export type ScannerCategories = {
  images: number
  pages: number
  data: number
  videos: number
  audio: number
  documents: number
  archives: number
  other: number
}

export type ExtensionSummary = {
  extension: string
  count: number
}

export type ScanError = {
  path: string
  message: string
}


export type ScannerFile = {
  relativePath: string
  absolutePath: string
  directory: string
  filename: string
  extension: string
  category: string
  size: number
  createdAt: string | null
  modifiedAt: string | null
  readable: boolean
  isDirectory: false
}

export type ScannerFolder = {
  absolutePath: string
  relativePath: string
  name: string
  parent: string | null
  depth: number
  readable: boolean
  isDirectory: true
}
export type ScannerResponse = {
  status: string
  workspacePath: string
  startedAt: string
  finishedAt: string
  durationMs: number
  totalFiles: number
  totalDirectories: number
  totalBytes: number
  categories: ScannerCategories
  extensions: ExtensionSummary[]
  errors: ScanError[]
  message: string
}

export type ScannerRequest = {
  workspacePath: string
}
