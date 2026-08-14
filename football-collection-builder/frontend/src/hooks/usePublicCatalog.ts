import{useCallback,useEffect,useRef,useState}from'react'
import*as api from'../services/publicCatalogService'
import type{PublicEntity,PublicPage,PublicSearchResult,PublicStatusResponse,PublicSummary}from'../types/publicCatalog'

export type PublicCatalogTab='countries'|'teams'|'collections'|'items'
type Selection={slug:string;name:string}
const empty:PublicPage={items:[],total:0,limit:24,offset:0,hasNext:false}

export default function usePublicCatalog(){
 const[statusInfo,setStatusInfo]=useState<PublicStatusResponse|null>(null),[summary,setSummary]=useState<PublicSummary|null>(null),[data,setData]=useState(empty),[latest,setLatest]=useState<PublicEntity[]>([])
 const[tab,setTabState]=useState<PublicCatalogTab>('countries'),[offset,setOffset]=useState(0),[search,setSearchState]=useState(''),[filterStatus,setFilterStatusState]=useState('')
 const[country,setCountry]=useState<Selection|null>(null),[team,setTeam]=useState<Selection|null>(null),[collection,setCollection]=useState<Selection|null>(null)
 const[searchResults,setSearchResults]=useState<PublicSearchResult[]>([]),[detail,setDetail]=useState<(PublicEntity&{media:unknown[];breadcrumbs:Array<{type:string;slug:string;label:string}>})|null>(null)
 const[loading,setLoading]=useState(true),[building,setBuilding]=useState(false),[error,setError]=useState('');const requestId=useRef(0)
 const refresh=useCallback(async(id=++requestId.current)=>{setLoading(true);setError('');try{const s=await api.status();if(id!==requestId.current)return;setStatusInfo(s);if(s.viewAvailable){const[x,pageResult,l]=await Promise.all([api.summary(),api.page(tab,offset,search,filterStatus,country?.slug??'',team?.slug??'',collection?.slug??''),api.latest()]);if(id!==requestId.current)return;setSummary(x);setData(pageResult);setLatest(l.items)}else{setSummary(null);setData(empty)}}catch(e){if(id===requestId.current)setError(e instanceof Error?e.message:'Falha ao consultar modelo público.')}finally{if(id===requestId.current)setLoading(false)}},[tab,offset,search,filterStatus,country,team,collection])
 useEffect(()=>{const id=++requestId.current;const timer=setTimeout(()=>void refresh(id),250);return()=>clearTimeout(timer)},[refresh])
 const navigateTab=(next:PublicCatalogTab)=>{requestId.current++;setData(empty);setOffset(0);setDetail(null);if(next==='countries'){setTeam(null);setCollection(null)}else if(next==='teams'){setCollection(null)};setTabState(next)}
 const selectCountry=(x:PublicEntity)=>{setCountry({slug:x.slug,name:String(x.name)});setTeam(null);setCollection(null);navigateTab('teams')}
 const selectTeam=(x:PublicEntity)=>{setCountry({slug:String(x.countrySlug),name:country?.name??String(x.countrySlug)});setTeam({slug:x.slug,name:String(x.name)});setCollection(null);navigateTab('collections')}
 const selectCollection=(x:PublicEntity)=>{setCountry({slug:String(x.countrySlug),name:country?.name??String(x.countrySlug)});setTeam({slug:String(x.teamSlug),name:team?.name??String(x.teamSlug)});setCollection({slug:x.slug,name:String(x.name)});navigateTab('items')}
 const clearNavigation=()=>{requestId.current++;setCountry(null);setTeam(null);setCollection(null);setDetail(null);setSearchState('');setFilterStatusState('');setSearchResults([]);setOffset(0);setData(empty);setTabState('countries')}
 const build=async()=>{setBuilding(true);setError('');try{await api.build();const id=++requestId.current;await refresh(id)}catch(e){setError(e instanceof Error?e.message:'Falha ao gerar modelo.')}finally{setBuilding(false)}}
 const testSearch=async(q:string)=>setSearchResults((await api.search(q)).items);const open=async(x:PublicEntity)=>{if(x.publicRoute)setDetail(await api.itemDetail(x.publicRoute))}
 return{statusInfo,summary,data,latest,tab,navigateTab,offset,setOffset,search,setSearch:(x:string)=>{setSearchState(x);setOffset(0)},filterStatus,setFilterStatus:(x:string)=>{setFilterStatusState(x);setOffset(0)},country,team,collection,selectCountry,selectTeam,selectCollection,clearNavigation,searchResults,testSearch,detail,setDetail,loading,building,error,build,open}
}
