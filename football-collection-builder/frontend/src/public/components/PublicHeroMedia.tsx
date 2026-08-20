import { useState } from 'react'
import { Link } from 'react-router-dom'
import type { PublicHeroMediaConfig } from '../config/publicSiteConfig'

export default function PublicHeroMedia({media}:{media:PublicHeroMediaConfig}){
 const[failed,setFailed]=useState(false)
 return <div className="public-hero-composition">
  {!failed?<><img className="public-hero-image" src={media.src} alt={media.alt} width={media.width} height={media.height} loading="eager" onError={()=>setFailed(true)}/><Link className="public-hero-cta-hitbox" to="/site/paises" aria-label="Explorar o acervo"><span>Explorar o acervo</span></Link></>:<div className="public-hero-fallback" role="img" aria-label="Football Collection"><span>Football Collection</span></div>}
 </div>
}
