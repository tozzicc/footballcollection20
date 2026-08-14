/* eslint-disable react-hooks/refs */
import { useEffect, useRef, useState } from 'react'

export function usePublicData<T>(loader:()=>Promise<T>,dependencies:unknown[]) {
 const key=JSON.stringify(dependencies)
 const loaderRef=useRef(loader);loaderRef.current=loader
 const [state,setState]=useState<{key:string;data:T|null;error:boolean}>({key:'',data:null,error:false})
 useEffect(()=>{let active=true;loaderRef.current().then(data=>{if(active)setState({key,data,error:false})}).catch(()=>{if(active)setState({key,data:null,error:true})});return()=>{active=false}},[key])
 return {data:state.key===key?state.data:null,loading:state.key!==key,error:state.key===key&&state.error}
}

export function usePageTitle(title:string){useEffect(()=>{document.title=title==='Football Collection'?title:`${title} | Football Collection`},[title])}
