import {useCallback,useEffect,useState} from 'react'
import * as api from '../services/imageParserService'
import type {BrokenPage,ImageMetadata,ImagePage,ImageParserStatus} from '../types/imageParser'
const empty:ImagePage={items:[],total:0,limit:50,offset:0};const emptyBroken:BrokenPage={items:[],total:0,limit:50,offset:0}
export default function useImageParser(workspacePath:string){
 const [parserStatus,setParserStatus]=useState<ImageParserStatus|null>(null),[images,setImages]=useState(empty),[orphans,setOrphans]=useState(empty),[invalid,setInvalid]=useState(empty),[broken,setBroken]=useState(emptyBroken),[details,setDetails]=useState<ImageMetadata|null>(null)
 const [offset,setOffset]=useState(0),[search,setSearch]=useState(''),[status,setStatus]=useState(''),[format,setFormat]=useState(''),[loading,setLoading]=useState(true),[parsing,setParsing]=useState(false),[error,setError]=useState('')
 const refresh=useCallback(async()=>{setLoading(true);setError('');try{const s=await api.getImageStatus();setParserStatus(s);if(s.hasRun){const [a,b,c,d]=await Promise.all([api.getImages(offset,search,status,format),api.getOrphans(),api.getInvalid(),api.getBroken()]);setImages(a);setOrphans(b);setInvalid(c);setBroken(d)}}catch(e){setError(e instanceof Error?e.message:'Falha ao consultar o Parser de Imagens.')}finally{setLoading(false)}},[offset,search,status,format])
 useEffect(()=>{const t=setTimeout(()=>void refresh(),300);return()=>clearTimeout(t)},[refresh])
 const run=async()=>{setParsing(true);setError('');try{await api.runImageParser(workspacePath);setOffset(0);await refresh()}catch(e){setError(e instanceof Error?e.message:'Falha ao executar.')}finally{setParsing(false)}}
 return{parserStatus,images,orphans,invalid,broken,details,setDetails,offset,setOffset,search,setSearch,status,setStatus,format,setFormat,loading,parsing,error,refresh,run,open:async(id:number)=>setDetails(await api.getImage(id))}
}
