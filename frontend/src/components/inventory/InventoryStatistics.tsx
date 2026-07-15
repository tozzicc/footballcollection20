import type { Inventory } from '../../types/inventory'
import SectionCard from '../ui/SectionCard'

const labels: Record<string, string> = { images: 'Imagens', pages: 'Páginas', videos: 'Vídeos', documents: 'Documentos', archives: 'Compactados', data: 'Dados', audio: 'Áudios', other: 'Outros' }
const InventoryStatistics = ({ inventory }: { inventory: Inventory }) => (
  <SectionCard title="Categorias" description="Distribuição dos arquivos classificados pelo Scanner.">
    <div className="inventory-table-scroll"><table className="inventory-table"><thead><tr><th>Categoria</th><th>Quantidade</th></tr></thead><tbody>{inventory.categories.slice(0, 50).map((row) => <tr key={row.category}><td>{labels[row.category] ?? row.category}</td><td>{row.count}</td></tr>)}</tbody></table></div>
  </SectionCard>
)
export default InventoryStatistics