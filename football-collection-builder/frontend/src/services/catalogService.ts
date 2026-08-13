import {ApiClient} from './apiClient'
import type {CatalogCountry,CatalogItem,CatalogIssue,CatalogPage,CatalogRun,CatalogStatus,CatalogSummary,CatalogTeam,ItemDetail,TeamDetail} from '../types/catalog'
const client=new ApiClient(),buildClient=new ApiClient({timeoutMs:900_000})
const qs=(o:Record<string,string|number|undefined>)=>{const p=new URLSearchParams();Object.entries(o).forEach(([k,v])=>{if(v!==undefined&&v!=='')p.set(k,String(v))});return p}
export const status=()=>client.get<CatalogStatus>('/api/catalog/status')
export const summary=()=>client.get<CatalogSummary>('/api/catalog/summary')
export const build=()=>buildClient.post<CatalogRun>('/api/catalog/build',{replacePrevious:true})
export const countries=(offset=0,search='')=>client.get<CatalogPage<CatalogCountry>>(`/api/catalog/countries?${qs({limit:50,offset,search})}`)
export const teams=(offset=0,search='',countryId='')=>client.get<CatalogPage<CatalogTeam>>(`/api/catalog/teams?${qs({limit:50,offset,search,countryId})}`)
export const items=(offset=0,search='',teamId?:number)=>client.get<CatalogPage<CatalogItem>>(`/api/catalog/items?${qs({limit:50,offset,search,teamId})}`)
export const issues=(offset=0,issueType='',severity='')=>client.get<CatalogPage<CatalogIssue>>(`/api/catalog/issues?${qs({limit:50,offset,issueType,severity})}`)
export const team=(id:number)=>client.get<TeamDetail>(`/api/catalog/teams/${id}`)
export const item=(id:number)=>client.get<ItemDetail>(`/api/catalog/items/${id}`)
