import { useParams } from 'react-router-dom'
import PublicBreadcrumbs from '../components/PublicBreadcrumbs'
import { PublicTeamCard } from '../components/PublicCards'
import { PublicCountryLogo } from '../components/PublicIdentityMedia'
import { PublicEmpty,PublicError,PublicLoading } from '../components/PublicStates'
import { usePageTitle,usePublicData } from '../hooks/usePublicData'
import { publicSiteService as api } from '../services/publicSiteService'
import { countryDisplayName } from '../utils/countryDisplayName'

export default function PublicCountryAllTeamsPage(){
 const{countrySlug=''}=useParams(),x=usePublicData(async()=>{const[detail,teams]=await Promise.all([api.getCountry(countrySlug),api.getAllTeamsByCountry(countrySlug)]);return{detail,teams}},[countrySlug])
 usePageTitle(x.data?countryDisplayName(x.data.detail.country.slug||x.data.detail.country.name):'País')
 if(x.loading)return <PublicLoading/>;if(x.error)return <PublicError/>;if(!x.data)return <PublicEmpty/>
 const{detail,teams}=x.data,displayName=countryDisplayName(detail.country.slug||detail.country.name)
 return <><PublicBreadcrumbs items={[{label:displayName}]}/><div className="public-detail-hero public-identity-hero"><div><header className="public-page-header"><p className="public-kicker">Acervo</p><h1>{displayName}</h1></header><p>{detail.summary.teams} equipes · {detail.summary.collections} coleções · {detail.summary.items} itens</p></div><PublicCountryLogo variant="header" media={detail.country.logoMedia} name={displayName}/></div><section className="public-section"><div className="public-section-heading"><h2>Equipes</h2></div><div className="public-card-grid public-team-grid">{teams.map(i=><PublicTeamCard key={i.slug} item={i}/>)}</div></section></>
}
