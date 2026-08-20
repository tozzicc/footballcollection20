import { Link, useParams } from 'react-router-dom'
import PublicBreadcrumbs from '../components/PublicBreadcrumbs'
import PublicEditorialRecord from '../components/PublicEditorialRecord'
import { usePageTitle, usePublicData } from '../hooks/usePublicData'
import { publicSiteService as api } from '../services/publicSiteService'
import type { PublicItem } from '../types'

type MemorialShirt = {
 title:string
 context:string
 load:()=>Promise<PublicItem>
}

const shirts:Record<string,MemorialShirt>={
 'sao-paulo':{
  title:'Chicão — São Paulo — 1977',
  context:'São Paulo',
  load:()=>api.getItemWithCollection('brasil','saopaulo','fot-gio','1977-5336f6'),
 },
 'selecao-brasileira':{
  title:'Copa do Mundo da Argentina 1978 — Chicão',
  context:'Seleção Brasileira',
  load:()=>api.getItemWithoutCollection('brasil','selecaob','1978'),
 },
 'atletico-mg':{
  title:'Chicão — Atlético-MG — 1979',
  context:'Atlético-MG',
  load:()=>api.getItemWithCollection('brasil','atletico','10-12','1979-ae6fca'),
 },
}

export default function PublicChicaoShirtMemorialPage(){
 const{memorialSlug=''}=useParams(),shirt=shirts[memorialSlug]
 const state=usePublicData(()=>shirt?shirt.load():Promise.reject(new Error('Memorial não encontrado')),[memorialSlug])
 usePageTitle(shirt?.title??'Camisa memorial não encontrada')
 if(!shirt)return <div className="public-not-found"><p className="public-kicker">404</p><h1>Camisa memorial não encontrada.</h1><Link className="public-cta" to="/site/chicao">Voltar ao memorial</Link></div>
 if(state.loading)return <div className="public-state"><div className="public-loader"/><p>Carregando acervo memorial…</p></div>
 if(state.error||!state.data)return <div className="public-state"><h1>Não foi possível carregar este registro memorial.</h1><Link className="public-cta" to="/site/chicao">Voltar ao memorial</Link></div>
 return <article>
  <PublicBreadcrumbs items={[{label:'Chicão — O Deus da Raça',to:'/site/chicao'},{label:'Camisas'},{label:shirt.context}]}/>
  <h1 className="sr-only">{shirt.title}</h1>
  <div className="public-editorial-records"><PublicEditorialRecord record={state.data}/></div>
 </article>
}
