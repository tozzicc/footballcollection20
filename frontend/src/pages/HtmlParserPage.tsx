import { Link } from 'react-router-dom'
import HtmlParserActions from '../components/html-parser/HtmlParserActions'
import HtmlParserPageDetails from '../components/html-parser/HtmlParserPageDetails'
import HtmlParserPagesTable from '../components/html-parser/HtmlParserPagesTable'
import HtmlParserStatusCard from '../components/html-parser/HtmlParserStatusCard'
import HtmlParserSummary from '../components/html-parser/HtmlParserSummary'
import MissingReferencesTable from '../components/html-parser/MissingReferencesTable'
import EmptyState from '../components/ui/EmptyState'
import useHtmlParser from '../hooks/useHtmlParser'
import useWorkspace from '../hooks/useWorkspace'

const HtmlParserPage = () => {
  const { workspacePath } = useWorkspace()
  const parser = useHtmlParser(workspacePath)
  return <div className="page-base">
    <header className="page-header"><h1>Parser HTML</h1><p className="page-subtitle">Metadados e referencias de paginas legadas em modo somente leitura.</p></header>
    <div aria-live="polite">{parser.isLoading && <p>Carregando resultados...</p>}{parser.error && <p className="inventory-error">{parser.error}</p>}</div>
    {parser.status && !parser.status.inventoryAvailable
      ? <EmptyState title="Inventory necessario" description="Construa e salve o Inventory antes de executar o Parser HTML."
          action={<Link className="btn btn-primary" to="/inventory">Ir para Inventory</Link>} />
      : parser.status && <><HtmlParserStatusCard value={parser.status} />
        <HtmlParserActions disabled={!workspacePath} isParsing={parser.isParsing} onRun={() => void parser.run()} onRefresh={() => void parser.refresh()} />
        {parser.status.lastRun ? <><HtmlParserSummary value={parser.status.lastRun} />
          <HtmlParserPagesTable value={parser.pages} search={parser.search} offset={parser.pageOffset}
            onSearch={(v) => { parser.setSearch(v); parser.setPageOffset(0) }} onOffset={parser.setPageOffset} onSelect={(id) => void parser.openDetails(id)} />
          <MissingReferencesTable value={parser.missing} offset={parser.missingOffset} onOffset={parser.setMissingOffset} />
        </> : <EmptyState title="Nenhuma execucao" description="HTML, HTM e ASP do Inventory serao analisados sem alterar o Workspace." />}</>}
    {parser.details && <HtmlParserPageDetails value={parser.details} onClose={() => parser.setDetails(null)} />}
  </div>
}
export default HtmlParserPage
