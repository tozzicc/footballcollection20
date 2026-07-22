import { Link } from 'react-router-dom'
import InventoryExtensions from '../components/inventory/InventoryExtensions'
import InventoryFolderTree from '../components/inventory/InventoryFolderTree'
import InventoryStatistics from '../components/inventory/InventoryStatistics'
import InventorySummary from '../components/inventory/InventorySummary'
import Button from '../components/ui/Button'
import SectionCard from '../components/ui/SectionCard'
import StatusBadge from '../components/ui/StatusBadge'
import useInventory from '../hooks/useInventory'
import useInventoryRepository from '../hooks/useInventoryRepository'
import useWorkspace from '../hooks/useWorkspace'

const InventoryPage = () => {
  const { workspacePath, isConfigured } = useWorkspace()
  const { inventory, status, error, isBuilding, build } = useInventory()
  const { databaseStatus, saveResult, isSaving, repositoryError, save } = useInventoryRepository()
  const badge = status === 'completed'
    ? { status: 'success' as const, label: 'Concluído' }
    : status === 'error'
      ? { status: 'error' as const, label: 'Erro' }
      : status === 'building'
        ? { status: 'info' as const, label: 'Construindo' }
        : { status: 'warning' as const, label: 'Aguardando' }
  const lastSavedAt = databaseStatus.lastSavedAt
    ? new Date(databaseStatus.lastSavedAt).toLocaleString('pt-BR')
    : 'Nenhuma gravação'

  return <div className="page-base">
    <header className="page-header">
      <h1>Inventory</h1>
      <p className="page-subtitle">Fonte estruturada de dados construída a partir do Scanner.</p>
    </header>

    <div className="inventory-two-columns">
      <SectionCard title="Construir Inventory" description="Executa o Scanner uma vez e transforma seu resultado sem reler o Workspace.">
        <div className="inventory-actions">
          <StatusBadge {...badge} />
          <Button variant="primary" disabled={!isConfigured || isBuilding} onClick={() => void build(workspacePath)}>
            {isBuilding ? 'Construindo...' : 'Construir Inventory'}
          </Button>
        </div>
        <p className="panel-description">Workspace: {workspacePath || 'Não configurado'}</p>
        {!isConfigured && <Link to="/workspace" className="btn btn-secondary">Configurar Workspace</Link>}
        {error && <p className="inventory-error">{error}</p>}
      </SectionCard>

      <SectionCard title="Status do Banco" description="Persistência local do Inventory em SQLite.">
        <div className="inventory-database-header">
          <StatusBadge status={databaseStatus.databaseCreated ? 'success' : 'warning'} label={databaseStatus.databaseCreated ? 'Banco criado' : 'Banco não criado'} />
          <Button variant="secondary" disabled={!inventory || isSaving} onClick={() => inventory && void save(inventory)}>
            {isSaving ? 'Salvando...' : 'Salvar Inventory'}
          </Button>
        </div>
        <div className="inventory-database-details">
          <p>Última gravação: {lastSavedAt}</p>
          <p>Arquivos gravados: {databaseStatus.fileCount}</p>
          <p>Pastas gravadas: {databaseStatus.folderCount}</p>
        </div>
        {saveResult && <p className="inventory-success">{saveResult.message} {saveResult.fileCount} arquivos e {saveResult.folderCount} pastas em {saveResult.durationMs} ms.</p>}
        {repositoryError && <p className="inventory-error">{repositoryError}</p>}
      </SectionCard>
    </div>

    {inventory && <>
      <InventorySummary inventory={inventory} />
      <div className="inventory-two-columns">
        <InventoryStatistics inventory={inventory} />
        <InventoryExtensions inventory={inventory} />
      </div>
      <InventoryFolderTree inventory={inventory} />
      <SectionCard title="Primeiros arquivos" description="Até 50 itens do Inventory.">
        <div className="inventory-table-scroll">
          <table className="inventory-table inventory-files-table">
            <thead><tr><th>Arquivo</th><th>Caminho relativo</th><th>Extensão</th><th>Categoria</th><th>Tamanho</th><th>Legível</th></tr></thead>
            <tbody>{inventory.items.slice(0, 50).map((item) => <tr key={item.id}><td>{item.filename}</td><td>{item.relativePath}</td><td>{item.extension || '(sem extensão)'}</td><td>{item.category}</td><td>{item.size} B</td><td>{item.readable ? 'Sim' : 'Não'}</td></tr>)}</tbody>
          </table>
        </div>
      </SectionCard>
    </>}
  </div>
}

export default InventoryPage