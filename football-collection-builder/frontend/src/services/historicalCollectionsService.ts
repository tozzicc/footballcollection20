import { ApiClient } from './apiClient'
import type { HistoricalItem, HistoricalPage, HistoricalSection, HistoricalStatusResponse, HistoricalSummary } from '../types/historicalCollections'

const api = new ApiClient()
export const historicalCollectionsService = {
  status: () => api.get<HistoricalStatusResponse>('/api/historical-collections/status'),
  build: () => api.post<unknown>('/api/historical-collections/build', {}),
  summary: () => api.get<HistoricalSummary>('/api/public/collections/summary'),
  sections: () => api.get<{items:HistoricalSection[]}>('/api/public/collections/sections'),
  section: (section:string) => api.get<HistoricalSection>(`/api/public/collections/sections/${section}`),
  item: (section:string, slug:string) => api.get<HistoricalItem>(`/api/public/collections/sections/${section}/items/${slug}`),
  items: (section:string, options:{group?:string;category?:string;limit?:number;offset?:number}={}) => {
    const query = new URLSearchParams()
    if(options.group)query.set('group',options.group)
    if(options.category)query.set('category',options.category)
    query.set('limit',String(options.limit ?? 24));query.set('offset',String(options.offset ?? 0))
    return api.get<HistoricalPage>(`/api/public/collections/sections/${section}/items?${query}`)
  },
}
