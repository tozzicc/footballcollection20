export type ReferenceStatus = 'resolved' | 'missing' | 'external' | 'anchor' | 'ignored' | 'invalid'
export type ParseStatus = 'completed' | 'completed_with_errors' | 'failed'

export type HtmlParseSummary = {
  id: number | null; workspacePath: string; startedAt: string; finishedAt: string | null
  durationMs: number; status: ParseStatus; totalPages: number; parsedPages: number
  failedPages: number; imageReferences: number; internalLinks: number
  externalLinks: number; missingReferences: number; message: string
}
export type HtmlParserStatus = {
  hasRun: boolean; inventoryAvailable: boolean; availablePages: number
  lastRun: HtmlParseSummary | null
}
export type HtmlParseResponse = HtmlParseSummary & { runId: number; errors: HtmlParseError[] }
export type HtmlParseError = { inventoryItemId: string | null; relativePath: string; errorType: string; message: string }
export type HtmlHeading = { level: number; position: number; text: string }
export type HtmlImageReference = {
  srcOriginal: string; srcNormalized: string; alt: string | null; title: string | null
  widthDeclared: string | null; heightDeclared: string | null; isExternal: boolean
  resolvedRelativePath: string | null; resolvedAbsolutePath: string | null
  existsInInventory: boolean; referencedInventoryItemId: string | null; status: ReferenceStatus
}
export type HtmlLinkReference = {
  hrefOriginal: string; hrefNormalized: string; visibleText: string | null; title: string | null
  isExternal: boolean; isAnchor: boolean; isMailto: boolean; isJavascript: boolean
  resolvedRelativePath: string | null; existsInInventory: boolean
  referencedInventoryItemId: string | null; status: ReferenceStatus
}
export type HtmlPageListItem = {
  id: number; relativePath: string; filename: string; title: string; encodingUsed: string | null
  imageReferences: number; linkReferences: number; missingReferences: number; parseStatus: string
}
export type HtmlPagesResponse = { items: HtmlPageListItem[]; total: number; limit: number; offset: number }
export type HtmlPageDetails = {
  id: number; inventoryItemId: string; relativePath: string; absolutePath: string; filename: string
  extension: string; fileSize: number; createdAt: string | null; modifiedAt: string | null
  encodingUsed: string | null; title: string; documentLanguage: string | null
  charsetDeclared: string | null; metaDescription: string | null; textPreview: string
  parseStatus: string; parseMessage: string; headings: HtmlHeading[]
  imageReferences: HtmlImageReference[]; linkReferences: HtmlLinkReference[]; errors: HtmlParseError[]
}
export type MissingReference = {
  id: number; pageId: number; sourceRelativePath: string; referenceType: 'image' | 'link'
  original: string; resolvedRelativePath: string | null; status: ReferenceStatus
}
export type MissingReferencesResponse = { items: MissingReference[]; total: number; limit: number; offset: number }
