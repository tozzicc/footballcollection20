import EmptyState from '../components/ui/EmptyState'
import { Link } from 'react-router-dom'

const ReportsPage = () => (
  <div className="page-base">
    <h1>Relatórios</h1>
    <p className="page-subtitle">Integridade, duplicidades e arquivos órfãos</p>

    <EmptyState
      title="Módulo de Relatórios em preparação"
      description="Aqui serão implementadas visões e relatórios de integridade, duplicidades e arquivos órfãos."
      action={<Link to="/dashboard" className="btn btn-secondary">Voltar ao Dashboard</Link>}
    />
  </div>
)

export default ReportsPage
