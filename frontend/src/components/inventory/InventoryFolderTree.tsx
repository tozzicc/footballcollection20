import type { Inventory } from '../../types/inventory'
import SectionCard from '../ui/SectionCard'

const InventoryFolderTree = ({ inventory }: { inventory: Inventory }) => (
  <SectionCard title="Primeiras pastas" description="Até 50 pastas na ordem produzida pelo Scanner.">
    <div className="inventory-table-scroll"><table className="inventory-table inventory-wide-table"><thead><tr><th>Pasta</th><th>Caminho relativo</th><th>Pasta pai</th><th>Profundidade</th></tr></thead><tbody>{inventory.folders.slice(0, 50).map((folder) => <tr key={folder.path}><td>{folder.name}</td><td>{folder.relativePath}</td><td>{folder.parent ?? '—'}</td><td>{folder.depth}</td></tr>)}</tbody></table></div>
  </SectionCard>
)
export default InventoryFolderTree