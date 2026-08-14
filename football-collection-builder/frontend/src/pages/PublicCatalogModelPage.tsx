import { useState } from 'react'
import Button from '../components/ui/Button'
import EmptyState from '../components/ui/EmptyState'
import SectionCard from '../components/ui/SectionCard'
import usePublicCatalog, { type PublicCatalogTab } from '../hooks/usePublicCatalog'
import type { PublicEntity, PublicMedia } from '../types/publicCatalog'

const tabs: Array<[PublicCatalogTab, string]> = [['countries', 'Países/regiões'], ['teams', 'Equipes'], ['collections', 'Collections'], ['items', 'Items']]
const text = (entity: PublicEntity, key: string) => String(entity[key] ?? '—')
const Preview = ({ media, large = false }: { media?: PublicMedia | null; large?: boolean }) => media?.mediaUrl
  ? <img loading="lazy" className={large ? 'media-layer-detail' : 'media-layer-preview'} src={media.mediaUrl} alt={media.altText ?? media.filename} />
  : <span>{media?.filename ?? 'Mídia ainda não preparada'}</span>

export default function PublicCatalogModelPage() {
  const p = usePublicCatalog()
  const [query, setQuery] = useState('')
  const select = (entity: PublicEntity) => {
    if (p.tab === 'countries') p.selectCountry(entity)
    else if (p.tab === 'teams') p.selectTeam(entity)
    else if (p.tab === 'collections') p.selectCollection(entity)
    else void p.open(entity)
  }
  const breadcrumb = `País: ${p.country?.name ?? 'todos'} → Equipe: ${p.team?.name ?? 'todas'}${p.collection ? ` → Collection: ${p.collection.name}` : ''}`
  return <div className="page-base">
    <header className="page-header"><h1>Modelo do Site</h1><p className="page-subtitle">Estrutura de apresentação preparada para o novo Football Collection.</p><p>Esta camada é derivada do catálogo normalizado e não altera o acervo original. Não representa ainda o site público final.</p></header>
    <div aria-live="polite">{p.loading && <p>Carregando modelo...</p>}{p.building && <p role="status">Preparando dados para apresentação...</p>}{p.error && <p className="inventory-error">{p.error}</p>}</div>
    {p.statusInfo && <>
      <SectionCard title="Status"><div className="parser-metrics">{[['Normalização disponível', p.statusInfo.normalizationAvailable ? 'Sim' : 'Não'], ['Modelo público disponível', p.statusInfo.viewAvailable ? 'Sim' : 'Não'], ['Última geração', p.statusInfo.lastRun ? new Date(String(p.statusInfo.lastRun.completedAt)).toLocaleString('pt-BR') : '—'], ['Versão do schema', p.statusInfo.schemaVersion]].map(([label, value]) => <div className="card-surface" key={String(label)}><span>{label}</span><strong>{value}</strong></div>)}</div><Button variant="primary" disabled={!p.statusInfo.normalizationAvailable || p.building} onClick={() => void p.build()}>{p.building ? 'Preparando dados...' : 'Gerar Modelo do Site'}</Button></SectionCard>
      {p.summary ? <>
        <SectionCard title="Resumo"><div className="parser-metrics">{[['Países/regiões', p.summary.countries], ['Equipes', p.summary.teams], ['Collections', p.summary.collections], ['Items', p.summary.items], ['Relações com mídia', p.summary.mediaRelations], ['Ready', p.summary.ready], ['Review Required', p.summary.reviewRequired], ['Unavailable', p.summary.unavailable], ['Duração', `${p.summary.durationMs} ms`]].map(([label, value]) => <div className="card-surface" key={String(label)}><span>{label}</span><strong>{typeof value === 'number' ? value.toLocaleString('pt-BR') : value}</strong></div>)}</div></SectionCard>
        <SectionCard title="Preview hierárquico" description={breadcrumb}>
          <div className="parser-actions">{tabs.map(([id, label]) => <Button key={id} variant={p.tab === id ? 'primary' : 'secondary'} onClick={() => p.navigateTab(id)}>{label}</Button>)}<Button onClick={() => { setQuery(''); p.clearNavigation() }}>Limpar navegação</Button></div>
          <div className="catalog-quality-filters"><label>Busca<input value={p.search} onChange={event => p.setSearch(event.target.value)} /></label><label>Status<select value={p.filterStatus} onChange={event => p.setFilterStatus(event.target.value)}><option value="">Todos</option><option>ready</option><option>review_required</option><option>unavailable</option></select></label></div>
          <div className="inventory-table-scroll"><table className="inventory-table"><thead><tr><th>Nome/título</th><th>Slug</th><th>Status</th><th>Mídia principal</th><th>Rota pública</th><th>Ação</th></tr></thead><tbody>{p.data.items.map(entity => <tr key={`${p.tab}-${entity.slug}-${String(entity.publicRoute)}`}><td>{String(entity.title ?? entity.name)}</td><td>{entity.slug}</td><td>{entity.publicStatus}</td><td><Preview media={entity.primaryMedia} /></td><td>{text(entity, 'publicRoute')}</td><td><Button onClick={() => select(entity)}>{p.tab === 'items' ? 'Preview' : 'Selecionar'}</Button></td></tr>)}</tbody></table></div>
          <div className="parser-pagination"><Button disabled={!p.offset} onClick={() => p.setOffset(Math.max(0, p.offset - 24))}>Anterior</Button><span>{p.data.total ? `${p.offset + 1}–${Math.min(p.offset + 24, p.data.total)} de ${p.data.total}` : '0 resultados'}</span><Button disabled={!p.data.hasNext} onClick={() => p.setOffset(p.offset + 24)}>Próxima</Button></div>
        </SectionCard>
        <SectionCard title="Testar busca pública"><div className="parser-actions"><input value={query} onChange={event => setQuery(event.target.value)} placeholder="País, equipe, collection ou item" /><Button disabled={!query.trim()} onClick={() => void p.testSearch(query)}>Buscar</Button></div><ul>{p.searchResults.map((result, index) => <li key={`${result.type}-${result.title}-${index}`}><Preview media={result.primaryMedia} /> <strong>{result.type}:</strong> {result.title} · {result.status}{result.publicRoute ? ` · ${result.publicRoute}` : ''}</li>)}</ul></SectionCard>
        <SectionCard title="Últimas inclusões"><div className="inventory-table-scroll"><table className="inventory-table"><thead><tr><th>Preview</th><th>Collection</th><th>Equipe</th><th>Período</th><th>Status</th></tr></thead><tbody>{p.latest.map(entity => <tr key={`${entity.countrySlug}-${entity.teamSlug}-${entity.slug}`}><td><Preview media={entity.primaryMedia} /></td><td>{entity.name}</td><td>{String(entity.teamSlug)}</td><td>{text(entity, 'displayPeriod')}</td><td>{entity.publicStatus}</td></tr>)}</tbody></table></div></SectionCard>
      </> : <EmptyState title="Modelo público ainda não gerado" description="Use Gerar Modelo do Site após concluir a normalização." />}
    </>}
    {p.detail && <div className="dialog-backdrop" onMouseDown={() => p.setDetail(null)}><section className="dialog-panel parser-details" role="dialog" aria-modal="true" onMouseDown={event => event.stopPropagation()}><div className="parser-details-header"><h2>{p.detail.title}</h2><Button onClick={() => p.setDetail(null)}>Fechar</Button></div><Preview media={p.detail.primaryMedia} large /><p><strong>Breadcrumb:</strong> {p.detail.breadcrumbs.map(item => item.label).join(' → ')}</p><p><strong>Rota:</strong> {p.detail.publicRoute}</p><p><strong>País:</strong> {p.detail.countrySlug} · <strong>Equipe:</strong> {p.detail.teamSlug} · <strong>Collection:</strong> {p.detail.collectionSlug ?? 'sem collection'}</p><p><strong>Status:</strong> {p.detail.publicStatus}</p><h3>Outras mídias</h3><ul>{p.detail.media.map((media, index) => { const item = media as PublicMedia; return <li key={index}><Preview media={item} /> {item.filename} · {item.availabilityStatus}</li> })}</ul></section></div>}
  </div>
}
