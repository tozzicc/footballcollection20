import type { ScanError } from './scanner'

export type InventoryItem = {
  id: string
  relativePath: string
  absolutePath: string
  directory: string
  filename: string
  extension: string
  category: string
  size: number
  createdAt: string | null
  modifiedAt: string | null
  isDirectory: false
  readable: boolean
}

export type InventoryFolder = { path: string; relativePath: string; name: string; parent: string | null; depth: number }
export type InventoryStatistics = { totalFiles: number; totalDirectories: number; totalSize: number; totalImages: number; totalPages: number; totalVideos: number; totalDocuments: number; totalArchives: number; totalData: number; totalOther: number }
export type InventoryCategorySummary = { category: string; count: number }
export type InventoryExtensionSummary = { extension: string; count: number }
export type InventoryMetadata = { generatedAt: string; scannerVersion: string; workspacePath: string; durationMs: number }
export type Inventory = { metadata: InventoryMetadata; statistics: InventoryStatistics; folders: InventoryFolder[]; items: InventoryItem[]; categories: InventoryCategorySummary[]; extensions: InventoryExtensionSummary[]; errors: ScanError[] }
export type InventoryRequest = { workspacePath: string }