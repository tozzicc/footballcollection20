import SectionCard from '../ui/SectionCard'
import type { HtmlParseSummary } from '../../types/htmlParser'

const HtmlParserSummary = ({ value }: { value: HtmlParseSummary }) => {
  const metrics = [
    ['Paginas encontradas', value.totalPages], ['Processadas', value.parsedPages],
    ['Com falha', value.failedPages], ['Imagens', value.imageReferences],
    ['Links internos', value.internalLinks], ['Links externos', value.externalLinks],
    ['Referencias ausentes', value.missingReferences],
  ]
  return <SectionCard title="Resumo da ultima execucao" description={value.finishedAt ? new Date(value.finishedAt).toLocaleString('pt-BR') : ''}>
    <div className="parser-metrics">{metrics.map(([label, count]) =>
      <div className="card-surface" key={label}><span>{label}</span><strong>{Number(count).toLocaleString('pt-BR')}</strong></div>)}
      <div className="card-surface"><span>Duracao</span><strong>{(value.durationMs / 1000).toFixed(1)} s</strong></div>
    </div>
  </SectionCard>
}
export default HtmlParserSummary
