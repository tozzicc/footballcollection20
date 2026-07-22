import { Link } from 'react-router-dom'

const NotFoundPage = () => (
  <div className="page-base">
    <h1>Página não encontrada</h1>
    <p className="page-subtitle">A página requisitada não existe.</p>
    <div style={{ marginTop: '1rem' }}>
      <Link to="/dashboard" className="btn btn-secondary">Voltar ao Dashboard</Link>
    </div>
  </div>
)

export default NotFoundPage
