import type { PublicMedia } from '../types/publicCatalog'

export type { PublicMedia }
export interface PublicCountry { slug:string; name:string; teamsCount:number; collectionsCount:number; itemsCount:number; primaryMedia:PublicMedia|null }
export interface PublicTeam { slug:string; countrySlug:string; name:string; collectionsCount:number; itemsCount:number; imagesCount:number; latestInclusionPeriod:string|null; primaryMedia:PublicMedia|null }
export interface PublicCollection { slug:string; countrySlug:string; teamSlug:string; name:string; collectionType:string; inclusionMonth:number|null; inclusionYear:number|null; inclusionBatch:number|null; displayPeriod:string|null; itemsCount:number; imagesCount:number; primaryMedia:PublicMedia|null }
export interface Crumb { type:string; slug:string; label:string }
export interface PublicItem { slug:string; countrySlug:string; teamSlug:string; collectionSlug:string|null; title:string; itemType:string; imagesCount:number; publicRoute:string; primaryMedia:PublicMedia|null; media?:PublicMedia[]; breadcrumbs:Crumb[]; seasonLabel?:string|null; seasonStartYear?:number|null; seasonEndYear?:number|null; description?:string|null; competition?:string|null }
export interface PublicPage<T> { items:T[]; total:number; limit:number; offset:number; hasNext:boolean }
export interface PublicSummary { countries:number; teams:number; collections:number; items:number; mediaRelations:number }
export interface SearchResult { type:'country'|'team'|'collection'|'item'; title:string; subtitle?:string; countrySlug?:string|null; teamSlug?:string|null; collectionSlug?:string|null; itemSlug?:string|null; publicRoute?:string|null; primaryMedia:PublicMedia|null }
export interface CountryDetail { country:PublicCountry; summary:{teams:number;collections:number;items:number}; teams:PublicTeam[] }
export interface TeamDetail { team:PublicTeam; country:PublicCountry; latestCollections:PublicCollection[] }
export interface CollectionDetail { collection:PublicCollection; items:PublicPage<PublicItem> }
