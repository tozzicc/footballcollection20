import Button from '../ui/Button'
import SectionCard from '../ui/SectionCard'
import type { MissingReferencesResponse } from '../../types/htmlParser'

type Props = { value: MissingReferencesResponse; offset: number; onOffset: (v: number) => void }
const MissingReferencesTable = ({ value, offset, onOffset }: Props) => (
  <SectionCard title="Referencias ausentes" description="Apenas referencias internas nao localizadas no Inventory.">
    <div className="inventory-table-scroll"><table className="inventory-table parser-table">
      <caption className="sr-only">Referencias ausentes encontradas pelo parser</caption>
      <thead><tr><th>Pagina de origem</th><th>Tipo</th><th>Referencia</th><th>Caminho resolvido</th><th>Status</th></tr></thead>
      <tbody>{value.items.map((item) => <tr key={`${item.referenceType}-${item.id}`}>
        <td>{item.sourceRelativePath}</td><td>{item.referenceType}</td><td>{item.original}</td>
        <td>{item.resolvedRelativePath ?? '-'}</td><td>{item.status}</td>
      </tr>)}</tbody>
    </table></div>
    <div className="parser-pagination">
      <Button disabled={offset === 0} onClick={() => onOffset(Math.max(0, offset - 50))}>Anterior</Button>
      <span>{value.total ? offset + 1 : 0}-{Math.min(offset + 50, value.total)} de {value.total}</span>
      <Button disabled={offset + 50 >= value.total} onClick={() => onOffset(offset + 50)}>Proxima</Button>
    </div>
  </SectionCard>
)
export default MissingReferencesTable
