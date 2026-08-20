import { ApiClient } from '../../services/apiClient'
import type { CollectionDetail, CountryDetail, PublicCollection, PublicCountry, PublicItem, PublicPage, PublicSummary, PublicTeam, SearchResult, SeasonDetail, TeamDetail } from '../types'

const api=new ApiClient(), root='/api/public/catalog'
const qs=(values:Record<string,string|number|undefined>)=>{const p=new URLSearchParams();Object.entries(values).forEach(([k,v])=>v!==undefined&&v!==''&&p.set(k,String(v)));return p.toString()}
export const publicSiteService={
 getSummary:()=>api.get<PublicSummary>(`${root}/summary`),
 getCountries:(limit=100)=>api.get<PublicPage<PublicCountry>>(`${root}/countries?${qs({limit})}`),
 getCountry:(country:string)=>api.get<CountryDetail>(`${root}/countries/${country}`),
 getTeams:(options:{country?:string;search?:string;limit?:number;offset?:number}={})=>api.get<PublicPage<PublicTeam>>(`${root}/teams?${qs({limit:24,offset:0,...options})}`),
 getAllTeamsByCountry:async(country:string)=>{
  const first=await api.get<PublicPage<PublicTeam>>(`${root}/teams?${qs({country,limit:100,offset:0})}`),items=[...first.items]
  for(let offset=first.limit;offset<first.total;offset+=first.limit){const page=await api.get<PublicPage<PublicTeam>>(`${root}/teams?${qs({country,limit:first.limit,offset})}`);items.push(...page.items)}
  return items
 },
 getAllTeams:async()=>{
  const first=await api.get<PublicPage<PublicTeam>>(`${root}/teams?${qs({limit:100,offset:0})}`),items=[...first.items]
  for(let offset=first.limit;offset<first.total;offset+=first.limit){const page=await api.get<PublicPage<PublicTeam>>(`${root}/teams?${qs({limit:first.limit,offset})}`);items.push(...page.items)}
  return items
 },
 getTeam:(country:string,team:string)=>api.get<TeamDetail>(`${root}/teams/${country}/${team}`),
 getSeason:(country:string,team:string,season:string)=>api.get<SeasonDetail>(`${root}/seasons/${country}/${team}/${season}`),
 getCollections:(options:{country?:string;team?:string;limit?:number;offset?:number}={})=>api.get<PublicPage<PublicCollection>>(`${root}/collections?${qs({limit:24,offset:0,...options})}`),
 getCollection:(country:string,team:string,collection:string)=>api.get<CollectionDetail>(`${root}/collections/${country}/${team}/${collection}`),
 getItems:(options:{country?:string;team?:string;collection?:string;limit?:number;offset?:number}={})=>api.get<PublicPage<PublicItem>>(`${root}/items?${qs({limit:24,offset:0,...options})}`),
 getAllItemsByTeam:async(country:string,team:string)=>{
  const first=await api.get<PublicPage<PublicItem>>(`${root}/items?${qs({country,team,limit:100,offset:0})}`),items=[...first.items]
  for(let offset=first.limit;offset<first.total;offset+=first.limit){const page=await api.get<PublicPage<PublicItem>>(`${root}/items?${qs({country,team,limit:first.limit,offset})}`);items.push(...page.items)}
  return items
 },
 getItemWithCollection:(country:string,team:string,collection:string,item:string)=>api.get<PublicItem>(`${root}/items/${country}/teams/${team}/collections/${collection}/${item}`),
 getItemWithoutCollection:(country:string,team:string,item:string)=>api.get<PublicItem>(`${root}/items/${country}/teams/${team}/items/${item}`),
 search:(q:string,offset=0)=>api.get<PublicPage<SearchResult>>(`${root}/search?${qs({q,limit:24,offset})}`),
 latest:(country='')=>api.get<{items:Array<PublicItem&PublicCollection>}>(`${root}/latest?${qs({limit:24,country})}`),
 navigation:()=>api.get<unknown>(`${root}/navigation`),
}
