import EmptyState from '../components/ui/EmptyState'
import { Link } from 'react-router-dom'

const LogsPage = () => (
  <div className="page-base">
    <h1>Logs</h1>
    <p className="page-subtitle">Histórico de execuções do Builder</p>

    <EmptyState
      title="Módulo de Logs em preparação"
      description="Aqui será exibido o histórico de execuções e eventos do Builder."
      action={<Link to="/dashboard" className="btn btn-secondary">Voltar ao Dashboard</Link>}
    />
  </div>
)

export default LogsPage
