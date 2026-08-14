import { ApiClient } from '../../services/apiClient'
import type { CollectionDetail, CountryDetail, PublicCollection, PublicCountry, PublicItem, PublicPage, PublicSummary, PublicTeam, SearchResult, TeamDetail } from '../types'

const api=new ApiClient(), root='/api/public/catalog'
const qs=(values:Record<string,string|number|undefined>)=>{const p=new URLSearchParams();Object.entries(values).forEach(([k,v])=>v!==undefined&&v!==''&&p.set(k,String(v)));return p.toString()}
export const publicSiteService={
 getSummary:()=>api.get<PublicSummary>(`${root}/summary`),
 getCountries:(limit=100)=>api.get<PublicPage<PublicCountry>>(`${root}/countries?${qs({limit})}`),
 getCountry:(country:string)=>api.get<CountryDetail>(`${root}/countries/${country}`),
 getTeams:(options:{country?:string;search?:string;limit?:number;offset?:number}={})=>api.get<PublicPage<PublicTeam>>(`${root}/teams?${qs({limit:24,offset:0,...options})}`),
 getTeam:(country:string,team:string)=>api.get<TeamDetail>(`${root}/teams/${country}/${team}`),
 getCollections:(options:{country?:string;team?:string;limit?:number;offset?:number}={})=>api.get<PublicPage<PublicCollection>>(`${root}/collections?${qs({limit:24,offset:0,...options})}`),
 getCollection:(country:string,team:string,collection:string)=>api.get<CollectionDetail>(`${root}/collections/${country}/${team}/${collection}`),
 getItems:(options:{country?:string;team?:string;collection?:string;limit?:number;offset?:number}={})=>api.get<PublicPage<PublicItem>>(`${root}/items?${qs({limit:24,offset:0,...options})}`),
 getItemWithCollection:(country:string,team:string,collection:string,item:string)=>api.get<PublicItem>(`${root}/items/${country}/teams/${team}/collections/${collection}/${item}`),
 getItemWithoutCollection:(country:string,team:string,item:string)=>api.get<PublicItem>(`${root}/items/${country}/teams/${team}/items/${item}`),
 search:(q:string,offset=0)=>api.get<PublicPage<SearchResult>>(`${root}/search?${qs({q,limit:24,offset})}`),
 latest:(country='')=>api.get<{items:Array<PublicItem&PublicCollection>}>(`${root}/latest?${qs({limit:24,country})}`),
 navigation:()=>api.get<unknown>(`${root}/navigation`),
}
