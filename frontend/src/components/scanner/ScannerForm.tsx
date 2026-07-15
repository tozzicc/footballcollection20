import Button from '../ui/Button'
import type { ScannerStatus } from '../../types/scanner'

type ScannerFormProps = {
  workspacePath: string
  isScanning: boolean
  status: ScannerStatus
  onRunScan: () => void
}

const ScannerForm = ({ workspacePath, isScanning, status, onRunScan }: ScannerFormProps) => (
  <div className="card-surface">
    <div className="button-row scanner-actions">
      <Button variant="primary" onClick={onRunScan} disabled={isScanning || !workspacePath}>
        {isScanning ? 'Analisando acervo...' : 'Executar análise'}
      </Button>
    </div>
    <p className="panel-description scanner-status-copy">
      A análise é estritamente somente leitura. Nenhum arquivo, pasta ou metadado será alterado.
    </p>
    <p className="panel-description scanner-status-copy compact">
      Estado atual: {status === 'scanning' ? 'Em execução' : status === 'completed' ? 'Concluído' : status === 'error' ? 'Erro' : 'Aguardando'}
    </p>
  </div>
)

export default ScannerForm
