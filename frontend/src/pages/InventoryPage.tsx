import { Link } from 'react-router-dom'
import InventoryExtensions from '../components/inventory/InventoryExtensions'
import InventoryFolderTree from '../components/inventory/InventoryFolderTree'
import InventoryStatistics from '../components/inventory/InventoryStatistics'
import InventorySummary from '../components/inventory/InventorySummary'
import Button from '../components/ui/Button'
import SectionCard from '../components/ui/SectionCard'
import StatusBadge from '../components/ui/StatusBadge'
import useInventory from '../hooks/useInventory'
import useWorkspace from '../hooks/useWorkspace'

const InventoryPage = () => {
  const { workspacePath, isConfigured } = useWorkspace()
  const { inventory, status, error, isBuilding, build } = useInventory()
  const badge = status === 'completed' ? { status: 'success' as const, label: 'Concluído' } : status === 'error' ? { status: 'error' as const, label: 'Erro' } : status === 'building' ? { status: 'info' as const, label: 'Construindo' } : { status: 'warning' as const, label: 'Aguardando' }

  return <div className="page-base">
    <header className="page-header"><h1>Inventory</h1><p className="page-subtitle">Fonte estruturada de dados construída a partir do Scanner.</p></header>
    <SectionCard title="Construir Inventory" description="Executa o Scanner uma vez e transforma seu resultado sem reler o Workspace.">
      <div className="inventory-actions"><StatusBadge {...badge} /><Button variant="primary" disabled={!isConfigured || isBuilding} onClick={() => void build(workspacePath)}>{isBuilding ? 'Construindo...' : 'Construir Inventory'}</Button></div>
      <p className="panel-description">Workspace: {workspacePath || 'Não configurado'}</p>
      {!isConfigured && <Link to="/workspace" className="btn btn-secondary">Configurar Workspace</Link>}
      {error && <p className="inventory-error">{error}</p>}
    </SectionCard>
    {inventory && <>
      <InventorySummary inventory={inventory} />
      <div className="inventory-two-columns"><InventoryStatistics inventory={inventory} /><InventoryExtensions inventory={inventory} /></div>
      <InventoryFolderTree inventory={inventory} />
      <SectionCard title="Primeiros arquivos" description="Até 50 itens do Inventory."><div className="inventory-table-scroll"><table className="inventory-table inventory-files-table"><thead><tr><th>Arquivo</th><th>Caminho relativo</th><th>Extensão</th><th>Categoria</th><th>Tamanho</th><th>Legível</th></tr></thead><tbody>{inventory.items.slice(0, 50).map((item) => <tr key={item.id}><td>{item.filename}</td><td>{item.relativePath}</td><td>{item.extension || '(sem extensão)'}</td><td>{item.category}</td><td>{item.size} B</td><td>{item.readable ? 'Sim' : 'Não'}</td></tr>)}</tbody></table></div></SectionCard>
    </>}
  </div>
}
export default InventoryPage