export type HistoricalSectionKey = 'pennants' | 'flags' | 'memorabilia'
export type HistoricalStatus = 'ready' | 'review_required' | 'unavailable'
export interface HistoricalSection { section: HistoricalSectionKey; title: string; description: string; itemsCount: number; ready: number; reviewRequired: number; unavailable: number; groups?: Array<{groupKey:string;count:number}> }
export interface HistoricalItem { section: HistoricalSectionKey; groupKey?: string | null; title?: string | null; description?: string | null; category?: string | null; slug: string; status: HistoricalStatus; mediaUrl?: string | null; route: string }
export interface HistoricalPage { items: HistoricalItem[]; total: number; limit: number; offset: number; hasNext: boolean }
export interface HistoricalSummary { schemaVersion:string;status:string;totalItems:number;ready:number;reviewRequired:number;unavailable:number;completedAt:string;sections:HistoricalSection[] }
export interface HistoricalStatusResponse { available:boolean;schemaVersion:string;lastBuild:HistoricalSummary|null }
