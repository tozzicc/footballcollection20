import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import '../styles/public-site.css'

const links = [['/site', 'Início'], ['/site/paises', 'Países'], ['/site/equipes', 'Equipes'], ['/site/colecoes', 'Coleções'], ['/site/chicao', 'Homenagem'], ['/site/ultimas', 'Últimas inclusões']]

export default function PublicLayout() {
  const [open, setOpen] = useState(false), [query, setQuery] = useState('')
  const navigate = useNavigate()
  const submit = (event: FormEvent) => { event.preventDefault(); if (query.trim()) navigate(`/site/busca?q=${encodeURIComponent(query.trim())}`) }
  return <div className="public-site"><header className="public-header"><div className="public-header-inner">
    <Link className="public-wordmark" to="/site"><strong>Football Collection</strong><span>Coleção de camisas</span></Link>
    <button className="public-menu-button" aria-expanded={open} aria-controls="public-nav" onClick={() => setOpen(value => !value)}>Menu</button>
    <nav id="public-nav" className={open ? 'is-open' : ''} aria-label="Navegação principal">{links.map(([to, text]) => <NavLink key={to} end={to === '/site'} to={to} onClick={() => setOpen(false)}>{text}</NavLink>)}</nav>
    <form className="public-header-search" onSubmit={submit}><label className="sr-only" htmlFor="public-search">Buscar no acervo</label><input id="public-search" value={query} onChange={event => setQuery(event.target.value)} placeholder="Buscar no acervo"/><button>Buscar</button></form>
  </div></header><main className="public-main"><Outlet/></main><footer className="public-footer"><div><strong>Football Collection</strong><p>Uma coleção de camisas e histórias do futebol.</p></div><p>Primeira versão visual navegável · 2026</p></footer></div>
}
