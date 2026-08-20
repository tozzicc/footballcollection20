import { useState } from 'react'
import type { PublicMedia } from '../types'
import { resolveMediaUrl } from '../utils/resolveMediaUrl'

const initials=(value:string)=>value.replaceAll('_',' ').split(/\s+/).filter(Boolean).slice(0,2).map(x=>x[0]).join('').toUpperCase()
export function PublicTeamLogo({media,name,className='',variant='compact'}:{media?:PublicMedia|null;name:string;className?:string;variant?:'compact'|'header'}){
 const[failed,setFailed]=useState(false),url=resolveMediaUrl(media?.mediaUrl)
 if(!url||failed)return <div className={`public-media public-identity-fallback public-identity-${variant} ${className}`} role="img" aria-label={`Escudo não disponível: ${name}`}><span>{initials(name)||'FC'}</span></div>
 return <div className={`public-media public-logo-media public-identity-${variant} ${className}`}><img src={url} alt={media?.altText||`Escudo de ${name}`} loading="lazy" onError={()=>setFailed(true)}/></div>
}
export function PublicCountryLogo({media,name,className='',variant='compact'}:{media?:PublicMedia|null;name:string;className?:string;variant?:'compact'|'header'}){
 const[failed,setFailed]=useState(false),url=resolveMediaUrl(media?.mediaUrl)
 if(!url||failed)return <div className={`public-media public-country-unavailable public-identity-${variant} ${className}`} role="img" aria-label={`Identidade histórica não disponível: ${name}`}><span>Identidade histórica não disponível</span></div>
 return <div className={`public-media public-logo-media public-country-logo public-identity-${variant} ${className}`}><img src={url} alt={media?.altText||`Identidade histórica de ${name}`} loading="lazy" onError={()=>setFailed(true)}/></div>
}
