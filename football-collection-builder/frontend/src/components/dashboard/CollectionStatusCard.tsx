import StatusBadge from '../ui/StatusBadge'
import type { CollectionStatus } from '../../types/dashboard'

type CollectionStatusCardProps = {
  status: CollectionStatus
}

const CollectionStatusCard = ({ status }: CollectionStatusCardProps) => (
  <div className="collection-status-content">
    <div className="status-grid">
      <div className="status-item">
        <p className="status-label">Integridade geral</p>
        <div className="status-value-wrapper">
          <StatusBadge
            status={status.integrity === 'good' ? 'success' : 'warning'}
            label={status.integrity === 'good' ? 'Boa' : 'Atenção'}
          />
        </div>
      </div>

      <div className="status-item">
        <p className="status-label">Imagens válidas</p>
        <p className="status-value">{status.validImages.toLocaleString('pt-BR')}</p>
      </div>

      <div className="status-item">
        <p className="status-label">Arquivos ignorados</p>
        <p className="status-value">{status.ignoredFiles.toLocaleString('pt-BR')}</p>
      </div>

      <div className="status-item">
        <p className="status-label">Banco interno</p>
        <div className="status-value-wrapper">
          <StatusBadge
            status={status.internalBank === 'configured' ? 'success' : 'warning'}
            label={status.internalBank === 'configured' ? 'Configurado' : 'Não configurado'}
          />
        </div>
      </div>
    </div>
  </div>
)

export default CollectionStatusCard
