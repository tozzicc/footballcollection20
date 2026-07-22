import { ApiClient } from './apiClient'
import type {
  HtmlPageDetails, HtmlPagesResponse, HtmlParseResponse, HtmlParseSummary,
  HtmlParserStatus, MissingReferencesResponse,
} from '../types/htmlParser'

const client = new ApiClient({ timeoutMs: 600_000 })
const query = (values: Record<string, string | number | undefined>) => {
  const params = new URLSearchParams()
  Object.entries(values).forEach(([key, value]) => { if (value !== undefined && value !== '') params.set(key, String(value)) })
  return params.toString()
}
export const getHtmlParserStatus = () => client.get<HtmlParserStatus>('/api/html-parser/status')
export const getHtmlParserSummary = () => client.get<HtmlParseSummary>('/api/html-parser/summary')
export const parseHtml = (workspacePath: string) =>
  client.post<HtmlParseResponse>('/api/html-parser/parse', { workspacePath, replacePrevious: true })
export const getHtmlPages = (limit: number, offset: number, search?: string) =>
  client.get<HtmlPagesResponse>(`/api/html-parser/pages?${query({ limit, offset, search })}`)
export const getHtmlPage = (id: number) => client.get<HtmlPageDetails>(`/api/html-parser/pages/${id}`)
export const getMissingReferences = (limit: number, offset: number, referenceType?: 'image' | 'link') =>
  client.get<MissingReferencesResponse>(`/api/html-parser/missing-references?${query({ limit, offset, referenceType })}`)
