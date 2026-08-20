import { Link } from 'react-router-dom'
import type { PublicItem } from '../types'
import PublicMediaImage from './PublicMediaImage'

export default function PublicEditorialRecord({record,index=0}:{record:PublicItem;index?:number}){
 const title=record.description||`Registro ${index+1}`
 return <article className="public-editorial-record"><h2>{title}</h2><div className="public-editorial-media">{record.media?.map((media,n)=><a key={media.publicMediaKey||n} href={media.mediaUrl||undefined} target="_blank" rel="noreferrer" aria-label={`Abrir imagem ${n+1} de ${title}`}><PublicMediaImage media={media} alt={`${title}, imagem ${n+1}`}/></a>)}</div><Link className="public-record-link" to={`/site${record.publicRoute}`}>Ver registro individual →</Link></article>
}
