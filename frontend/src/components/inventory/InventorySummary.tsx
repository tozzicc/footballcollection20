import type { Inventory } from '../../types/inventory'
import SectionCard from '../ui/SectionCard'

const formatBytes = (value: number) => {
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let amount = value
  let unit = 0
  while (amount >= 1024 && unit < units.length - 1) { amount /= 1024; unit += 1 }
  return `${amount.toFixed(unit === 0 ? 0 : 1)} ${units[unit]}`
}

const InventorySummary = ({ inventory }: { inventory: Inventory }) => (
  <SectionCard title="Resumo" description="Visão consolidada produzida pelo Inventory Builder.">
    <div className="inventory-metrics">
      <div className="card-surface"><span>Arquivos</span><strong>{inventory.statistics.totalFiles}</strong></div>
      <div className="card-surface"><span>Pastas</span><strong>{inventory.statistics.totalDirectories}</strong></div>
      <div className="card-surface"><span>Imagens</span><strong>{inventory.statistics.totalImages}</strong></div>
      <div className="card-surface"><span>Páginas</span><strong>{inventory.statistics.totalPages}</strong></div>
      <div className="card-surface"><span>Tamanho total</span><strong>{formatBytes(inventory.statistics.totalSize)}</strong></div>
      <div className="card-surface"><span>Tempo da análise</span><strong>{inventory.metadata.durationMs} ms</strong></div>
    </div>
  </SectionCard>
)
export default InventorySummary