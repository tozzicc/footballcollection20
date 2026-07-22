import type { Inventory } from '../../types/inventory'
import SectionCard from '../ui/SectionCard'

const InventoryExtensions = ({ inventory }: { inventory: Inventory }) => (
  <SectionCard title="Extensões" description="Até 50 extensões encontradas, ordenadas pelo Scanner.">
    <div className="inventory-table-scroll"><table className="inventory-table"><thead><tr><th>Extensão</th><th>Quantidade</th></tr></thead><tbody>{inventory.extensions.slice(0, 50).map((row) => <tr key={row.extension}><td>{row.extension || '(sem extensão)'}</td><td>{row.count}</td></tr>)}</tbody></table></div>
  </SectionCard>
)
export default InventoryExtensions