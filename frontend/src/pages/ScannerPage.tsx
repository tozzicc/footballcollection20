import EmptyState from '../components/ui/EmptyState'
import { Link } from 'react-router-dom'

const ScannerPage = () => (
  <div className="page-base">
    <h1>Scanner</h1>
    <p className="page-subtitle">Leitura e análise do acervo</p>

    <EmptyState
      title="Módulo do Scanner em preparação"
      description="Nesta página serão implementadas as ferramentas de leitura e análise do acervo."
      action={<Link to="/dashboard" className="btn btn-secondary">Voltar ao Dashboard</Link>}
    />
  </div>
)

export default ScannerPage
