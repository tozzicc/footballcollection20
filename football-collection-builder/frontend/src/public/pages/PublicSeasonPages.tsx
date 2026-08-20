import { Link,useParams } from 'react-router-dom'
import PublicBreadcrumbs from '../components/PublicBreadcrumbs'
import PublicEditorialRecord from '../components/PublicEditorialRecord'
import { PublicTeamLogo } from '../components/PublicIdentityMedia'
import { PublicEmpty,PublicError,PublicLoading } from '../components/PublicStates'
import { usePageTitle,usePublicData } from '../hooks/usePublicData'
import { publicSiteService as api } from '../services/publicSiteService'
import type { PublicItem } from '../types'
import { teamDisplayName } from '../utils/teamDisplayName'
import { countryDisplayName } from '../utils/countryDisplayName'

const Gate=({x,children}:{x:{loading:boolean;error:boolean;data:unknown};children:React.ReactNode})=>x.loading?<PublicLoading/>:x.error?<PublicError/>:!x.data?<PublicEmpty/>:<>{children}</>

export function PublicTeamSeasonsPage(){
 const{countrySlug='',teamSlug=''}=useParams()
 const x=usePublicData(async()=>{const[detail,items]=await Promise.all([api.getTeam(countrySlug,teamSlug),api.getAllItemsByTeam(countrySlug,teamSlug)]);return{detail,items}},[countrySlug,teamSlug])
 usePageTitle(x.data?teamDisplayName(x.data.detail.team):'Equipe')
 const grouped=new Map<string,PublicItem[]>(),other:PublicItem[]=[]
 for(const item of x.data?.items||[]){if(item.seasonLabel){const rows=grouped.get(item.seasonLabel)||[];rows.push(item);grouped.set(item.seasonLabel,rows)}else other.push(item)}
 const seasons=[...grouped.entries()].sort((a,b)=>(b[1][0].seasonStartYear||0)-(a[1][0].seasonStartYear||0)||b[0].localeCompare(a[0]))
 const displayName=x.data?teamDisplayName(x.data.detail.team):''
 return <Gate x={x}>{x.data&&<>
  <PublicBreadcrumbs items={[{label:countryDisplayName(countrySlug),to:`/site/paises/${countrySlug}`},{label:displayName}]}/>
  <div className="public-detail-hero public-identity-hero"><div><header className="public-page-header"><p className="public-kicker">{countryDisplayName(countrySlug)}</p><h1>{displayName}</h1></header><p>{x.data.detail.team.itemsCount} itens · {x.data.detail.team.imagesCount} imagens</p></div><PublicTeamLogo variant="header" media={x.data.detail.team.logoMedia} name={displayName}/></div>
  <section className="public-section"><div className="public-section-heading"><h2>Temporadas</h2></div><div className="public-season-grid">{seasons.map(([season,items])=><Link className="public-season-card" key={season} to={`temporadas/${encodeURIComponent(season)}`}><strong>{season}</strong><span>{items.length} {items.length===1?'registro':'registros'} · {items.reduce((n,i)=>n+i.imagesCount,0)} imagens</span></Link>)}</div></section>
  {other.length>0&&<section className="public-section"><div className="public-section-heading"><h2>Outros registros</h2></div><div className="public-season-grid">{other.map(i=><Link className="public-season-card" key={i.publicRoute} to={`/site${i.publicRoute}`}><strong>{i.title}</strong><span>{i.imagesCount} imagens</span></Link>)}</div></section>}
 </>}</Gate>
}

export function PublicSeasonPage(){
 const{countrySlug='',teamSlug='',season=''}=useParams()
 const x=usePublicData(()=>api.getSeason(countrySlug,teamSlug,season),[countrySlug,teamSlug,season])
 const displayName=x.data?teamDisplayName(x.data.team):''
 usePageTitle(x.data?`${displayName} ${x.data.season}`:'Temporada')
 return <Gate x={x}>{x.data&&<>
  <PublicBreadcrumbs items={[{label:countryDisplayName(countrySlug),to:`/site/paises/${countrySlug}`},{label:displayName,to:`/site/paises/${countrySlug}/equipes/${teamSlug}`},{label:x.data.season}]}/>
  <div className="public-season-header"><PublicTeamLogo variant="header" media={x.data.team.logoMedia} name={displayName}/><div><p className="public-kicker">{countryDisplayName(countrySlug)}</p><h1>{displayName}</h1><h2>{x.data.season}</h2><p>{x.data.summary.records} {x.data.summary.records===1?'registro':'registros'} · {x.data.summary.images} imagens</p></div></div>
  <div className="public-editorial-records">{x.data.records.map((record,index)=><PublicEditorialRecord record={record} index={index} key={record.publicRoute}/>)}</div>
 </>}</Gate>
}
