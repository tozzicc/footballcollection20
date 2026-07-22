import { Link } from 'react-router-dom'
import SectionCard from '../components/ui/SectionCard'
import { useScanner } from '../hooks/useScanner'
import useWorkspace from '../hooks/useWorkspace'
import ScannerForm from '../components/scanner/ScannerForm'
import ScannerStatus from '../components/scanner/ScannerStatus'
import ScannerSummary from '../components/scanner/ScannerSummary'
import ExtensionSummaryTable from '../components/scanner/ExtensionSummaryTable'

const ScannerPage = () => {
  const { workspace, isConfigured, workspacePath } = useWorkspace()
  const { runScan, scanResult, isScanning, scanError, resetScan, status } = useScanner()

  const handleRunScan = () => {
    if (!workspacePath.trim()) {
      return
    }
    void runScan(workspacePath)
  }

  const statusMessage = scanError
    ? scanError
    : status === 'scanning'
      ? 'Analisando o acervo em modo somente leitura. Não haverá alterações no sistema de arquivos.'
      : status === 'completed' && scanResult
        ? scanResult.message
        : 'Aguardando uma análise. O scanner executa apenas leitura e não altera o acervo.'

  return (
    <div className="page-base">
      <h1>Scanner</h1>
      <p className="page-subtitle">Leitura e análise do acervo</p>

      <SectionCard title="Workspace ativo" description="Use o workspace já configurado para executar a leitura real do acervo.">
        <div className="card-surface">
          <p className="panel-description">Caminho atual: {workspace.path || 'Não configurado'}</p>
          <p className="panel-description">Status: {isConfigured ? 'Configurado' : 'Não configurado'}</p>
          {!isConfigured && (
            <div style={{ marginTop: '1rem' }}>
              <Link to="/workspace" className="btn btn-secondary">Configurar Workspace</Link>
            </div>
          )}
        </div>
      </SectionCard>

      <ScannerStatus status={status} message={statusMessage} workspacePath={workspacePath} isConfigured={isConfigured} />
      <ScannerForm workspacePath={workspacePath} isScanning={isScanning} status={status} onRunScan={handleRunScan} />

      {status === 'completed' && scanResult && (
        <>
          <ScannerSummary result={scanResult} />
          <ExtensionSummaryTable result={scanResult} />
        </>
      )}

      {status === 'error' && (
        <SectionCard title="Erro da análise" description="A análise não pôde ser concluída.">
          <div className="card-surface">
            <p className="panel-description">{scanError}</p>
            <div style={{ marginTop: '1rem' }}>
              <button className="btn btn-secondary" type="button" onClick={resetScan}>Limpar erro</button>
            </div>
          </div>
        </SectionCard>
      )}
    </div>
  )
}

export default ScannerPage
