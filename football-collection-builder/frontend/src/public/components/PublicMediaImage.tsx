import { useState } from 'react'
import type { PublicMedia } from '../types'
import { resolveMediaUrl } from '../utils/resolveMediaUrl'

export default function PublicMediaImage({media,alt,className='',eager=false}:{media?:PublicMedia|null;alt:string;className?:string;eager?:boolean}){
 const[failedUrl,setFailedUrl]=useState<string|null>(null),url=resolveMediaUrl(media?.mediaUrl)
 if(!url||failedUrl===url)return <div className={`public-media public-media-fallback ${className}`} role="img" aria-label={`Imagem não disponível: ${alt}`}><span>FC</span></div>
 return <img className={`public-media ${className}`} src={url} alt={media?.altText||alt} loading={eager?'eager':'lazy'} onError={()=>setFailedUrl(url)}/>
}
