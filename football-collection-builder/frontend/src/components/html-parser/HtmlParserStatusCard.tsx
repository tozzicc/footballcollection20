import SectionCard from '../ui/SectionCard'
import StatusBadge from '../ui/StatusBadge'
import type { HtmlParserStatus } from '../../types/htmlParser'

const HtmlParserStatusCard = ({ value }: { value: HtmlParserStatus }) => (
  <SectionCard title="Status" description="O parser usa somente as paginas do Inventory persistido.">
    <div className="parser-status-line">
      <StatusBadge status={value.hasRun ? 'success' : 'warning'} label={value.hasRun ? 'Resultados disponiveis' : 'Aguardando'} />
      <strong>{value.availablePages.toLocaleString('pt-BR')} paginas disponiveis</strong>
    </div>
    <p className="panel-description">HTML, HTM e ASP sao lidos sem executar codigo ou alterar o acervo.</p>
  </SectionCard>
)
export default HtmlParserStatusCard
