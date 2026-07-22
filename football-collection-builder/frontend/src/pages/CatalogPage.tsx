import EmptyState from '../components/ui/EmptyState'
import { Link } from 'react-router-dom'

const CatalogPage = () => (
  <div className="page-base">
    <h1>Catálogo</h1>
    <p className="page-subtitle">Consulta de países, equipes e imagens</p>

    <EmptyState
      title="Módulo do Catálogo em preparação"
      description="Nesta página será possível consultar países, equipes e imagens do acervo."
      action={<Link to="/dashboard" className="btn btn-secondary">Voltar ao Dashboard</Link>}
    />
  </div>
)

export default CatalogPage
