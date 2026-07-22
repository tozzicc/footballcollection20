import StatusBadge from '../ui/StatusBadge'
import type { ScannerStatus as ScannerStatusType } from '../../types/scanner'

type ScannerStatusProps = {
  status: ScannerStatusType
  message: string
  workspacePath: string
  isConfigured: boolean
}

const statusConfig: Record<ScannerStatusType, { label: string; badge: 'success' | 'warning' | 'error' | 'info' }> = {
  idle: { label: 'Aguardando', badge: 'warning' },
  scanning: { label: 'Em execução', badge: 'info' },
  completed: { label: 'Concluído', badge: 'success' },
  error: { label: 'Erro', badge: 'error' },
}

const ScannerStatus = ({ status, message, workspacePath, isConfigured }: ScannerStatusProps) => (
  <div className="card-surface" aria-live="polite">
    <div className="badge-row scanner-badge-row">
      <StatusBadge status={statusConfig[status].badge} label={statusConfig[status].label} />
    </div>
    <p className="panel-description scanner-status-copy">{message}</p>
    <p className="panel-description scanner-status-copy compact">
      {isConfigured ? `Workspace atual: ${workspacePath}` : 'Nenhum workspace configurado. Configure um workspace para executar a análise.'}
    </p>
  </div>
)

export default ScannerStatus
