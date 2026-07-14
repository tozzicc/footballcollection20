import EmptyState from '../components/ui/EmptyState'
import { Link } from 'react-router-dom'

const SettingsPage = () => (
  <div className="page-base">
    <h1>Configurações</h1>
    <p className="page-subtitle">Caminhos do acervo, preferências e parâmetros</p>

    <EmptyState
      title="Módulo de Configurações em preparação"
      description="Nesta página serão definidos caminhos, preferências e parâmetros do Builder."
      action={<Link to="/dashboard" className="btn btn-secondary">Voltar ao Dashboard</Link>}
    />
  </div>
)

export default SettingsPage
