import EmptyState from '../components/ui/EmptyState'
import { Link } from 'react-router-dom'

const ExportsPage = () => (
  <div className="page-base">
    <h1>Exportações</h1>
    <p className="page-subtitle">Geração de JSON e arquivos para o Football Collection 2.0</p>

    <EmptyState
      title="Módulo de Exportação em preparação"
      description="Aqui serão implementadas ferramentas para gerar JSON e pacotes de exportação."
      action={<Link to="/dashboard" className="btn btn-secondary">Voltar ao Dashboard</Link>}
    />
  </div>
)

export default ExportsPage
