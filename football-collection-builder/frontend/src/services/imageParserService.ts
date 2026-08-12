import {ApiClient} from './apiClient'
import type {BrokenPage,ImageMetadata,ImagePage,ImageParserStatus,ImageSummary} from '../types/imageParser'
const client=new ApiClient(); const parseClient=new ApiClient({timeoutMs:900_000})
const qs=(x:Record<string,string|number|undefined>)=>{const p=new URLSearchParams();Object.entries(x).forEach(([k,v])=>{if(v!==undefined&&v!=='')p.set(k,String(v))});return p.toString()}
export const getImageStatus=()=>client.get<ImageParserStatus>('/api/image-parser/status')
export const getImageSummary=()=>client.get<ImageSummary>('/api/image-parser/summary')
export const runImageParser=(workspacePath:string)=>parseClient.post<ImageSummary>('/api/image-parser/parse',{workspacePath,replacePrevious:true})
export const getImages=(offset=0,search='',status='',format='')=>client.get<ImagePage>(`/api/image-parser/images?${qs({limit:50,offset,search,status,format})}`)
export const getImage=(id:number)=>client.get<ImageMetadata>(`/api/image-parser/images/${id}`)
export const getOrphans=(offset=0)=>client.get<ImagePage>(`/api/image-parser/orphans?limit=50&offset=${offset}`)
export const getInvalid=(offset=0)=>client.get<ImagePage>(`/api/image-parser/invalid?limit=50&offset=${offset}`)
export const getBroken=(offset=0)=>client.get<BrokenPage>(`/api/image-parser/broken-references?limit=50&offset=${offset}`)
