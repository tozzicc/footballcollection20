import { Link } from 'react-router-dom'
import { useState } from 'react'
import { resolveMediaUrl } from '../utils/resolveMediaUrl'

export function HistoricalEditorialCover({src,alt,title,className=''}:{src:string;alt:string;title:string;className?:string}){
 const[failed,setFailed]=useState(false)
 return failed?<div className={`historical-editorial-fallback ${className}`} role="img" aria-label={`Imagem não disponível: ${title}`}><span>{title}</span></div>:<img className={className} src={src} alt={alt} loading="lazy" onError={()=>setFailed(true)}/>
}

export default function HistoricalCollectionCard({title,description,mediaUrl,to,meta,imageAlt,editorialCover=false}:{title:string;description?:string|null;mediaUrl?:string|null;to?:string;meta?:string;imageAlt?:string;editorialCover?:boolean}){
 const[failed,setFailed]=useState(false),url=editorialCover?mediaUrl:resolveMediaUrl(mediaUrl)
 const content=<>{url&&!failed?<div className={`historical-card-media ${editorialCover?'historical-editorial-media':''}`}><img className="public-media" src={url} alt={imageAlt||title} loading="lazy" onError={()=>setFailed(true)}/></div>:<div className={`public-media historical-card-media ${editorialCover?'historical-editorial-fallback':'public-media-fallback'}`} role="img" aria-label={`Imagem não disponível: ${title}`}><span>{editorialCover?title:'FC'}</span></div>}<div>{meta&&<p className="public-kicker">{meta}</p>}<h3>{title}</h3>{description&&<p className="public-card-description">{description}</p>}</div></>
 return to?<Link className="public-card historical-card" to={to}>{content}</Link>:<article className="public-card historical-card">{content}</article>
}
