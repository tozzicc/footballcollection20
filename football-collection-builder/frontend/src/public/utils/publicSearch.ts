import type { PublicPage, PublicTeam, SearchResult } from '../types'
import { teamDisplayName } from './teamDisplayName.ts'

export const normalizePublicSearchTerm=(value:string)=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR').replace(/[^a-z0-9]+/g,' ').trim()

const sameIdentity=(query:string,value:string|null|undefined)=>{
 const a=normalizePublicSearchTerm(query),b=normalizePublicSearchTerm(value||'')
 return Boolean(a&&b&&(a===b||a.replaceAll(' ','')===b.replaceAll(' ','')))
}

const matchesTeamIdentity=(query:string,value:string|null|undefined)=>{
 const a=normalizePublicSearchTerm(query),b=normalizePublicSearchTerm(value||'')
 return sameIdentity(query,value)||Boolean(a&&b.split(' ').includes(a))
}

const key=(item:SearchResult)=>item.type==='editorial'?`editorial:${item.publicRoute}`:`${item.type}:${item.countrySlug||''}:${item.teamSlug||''}:${item.collectionSlug||''}:${item.itemSlug||''}`

export function publicSearchApiQueries(query:string,teams:PublicTeam[]):string[]{
 const aliases=teams.filter(team=>[teamDisplayName(team),team.name,team.slug].some(value=>sameIdentity(query,value))).map(team=>teamDisplayName(team))
 return [...new Set([query,...aliases].map(value=>value.trim()).filter(Boolean))]
}

export function mergePublicSearchResults(query:string,apiPage:PublicPage<SearchResult>,teams:PublicTeam[]):PublicPage<SearchResult>{
 const matchingTeams=teams.filter(team=>[teamDisplayName(team),team.name,team.slug].some(value=>matchesTeamIdentity(query,value)))
 const exactTeams=matchingTeams.filter(team=>[teamDisplayName(team),team.name,team.slug].some(value=>sameIdentity(query,value)))
 const teamResults=matchingTeams.map<SearchResult>(team=>({
  type:'team',title:teamDisplayName(team),subtitle:team.name,countrySlug:team.countrySlug,teamSlug:team.slug,primaryMedia:team.logoMedia||team.primaryMedia,
 }))
 const editorial:SearchResult[]=sameIdentity(query,'Chicão')?[{type:'editorial',title:'Chicão — O Deus da Raça',subtitle:'Homenagem',publicRoute:'/site/chicao',primaryMedia:null}]:[]
 const merged=[...editorial,...teamResults,...apiPage.items],seen=new Set<string>(),deduplicated=merged.filter(item=>{const identity=key(item);if(seen.has(identity))return false;seen.add(identity);return true})
 const exactTeam=exactTeams.length===1?exactTeams[0]:null
 const contextual=exactTeam?teamResults.filter(item=>item.countrySlug===exactTeam.countrySlug&&item.teamSlug===exactTeam.slug):matchingTeams.length?teamResults:sameIdentity(query,'Chicão')?deduplicated.filter(item=>item.type==='editorial'):deduplicated
 const rank=(item:SearchResult)=>{
  if(item.type==='editorial')return sameIdentity(query,'Chicão')?0:2
  if(item.type==='team')return [item.title,item.subtitle,item.teamSlug].some(value=>sameIdentity(query,value))?0:2
  if(exactTeam&&item.countrySlug===exactTeam.countrySlug&&item.teamSlug===exactTeam.slug)return 1
  return 3
 }
 const items=contextual.map((item,index)=>({item,index,rank:rank(item)})).sort((a,b)=>a.rank-b.rank||a.index-b.index).map(value=>value.item)
 return{items,total:items.length,limit:items.length,offset:0,hasNext:false}
}

export function publicSearchResultText(item:SearchResult,teams:PublicTeam[]):{title:string;subtitle:string|undefined}{
 if(item.type==='team')return{title:teamDisplayName({countrySlug:item.countrySlug,slug:item.teamSlug,name:item.title}),subtitle:item.subtitle}
 const owner=(item.type==='item'||item.type==='collection')?teams.find(team=>team.countrySlug===item.countrySlug&&team.slug===item.teamSlug):undefined
 return{title:item.title,subtitle:owner?`Equipe: ${teamDisplayName(owner)}`:item.subtitle}
}
