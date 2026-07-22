import Button from '../ui/Button'
import SectionCard from '../ui/SectionCard'
import StatusBadge from '../ui/StatusBadge'
import type { HtmlPagesResponse } from '../../types/htmlParser'

type Props = { value: HtmlPagesResponse; search: string; offset: number; onSearch: (v: string) => void; onOffset: (v: number) => void; onSelect: (id: number) => void }
const HtmlParserPagesTable = ({ value, search, offset, onSearch, onOffset, onSelect }: Props) => (
  <SectionCard title="Paginas analisadas" description="Resultados paginados do banco interno.">
    <label className="parser-search">Buscar pagina
      <input value={search} onChange={(event) => onSearch(event.target.value)} placeholder="Arquivo ou titulo" />
    </label>
    <div className="inventory-table-scroll"><table className="inventory-table parser-table">
      <caption className="sr-only">Paginas processadas pelo Parser HTML</caption>
      <thead><tr><th>Arquivo</th><th>Titulo</th><th>Encoding</th><th>Imagens</th><th>Links</th><th>Ausentes</th><th>Status</th></tr></thead>
      <tbody>{value.items.map((item) => <tr key={item.id}>
        <td><button className="parser-link-button" onClick={() => onSelect(item.id)}>{item.filename}</button></td>
        <td>{item.title}</td><td>{item.encodingUsed ?? '-'}</td><td>{item.imageReferences}</td>
        <td>{item.linkReferences}</td><td>{item.missingReferences}</td>
        <td><StatusBadge status={item.parseStatus === 'parsed' ? 'success' : 'error'} label={item.parseStatus} /></td>
      </tr>)}</tbody>
    </table></div>
    <div className="parser-pagination">
      <Button disabled={offset === 0} onClick={() => onOffset(Math.max(0, offset - 50))}>Anterior</Button>
      <span>{value.total ? offset + 1 : 0}-{Math.min(offset + 50, value.total)} de {value.total}</span>
      <Button disabled={offset + 50 >= value.total} onClick={() => onOffset(offset + 50)}>Proxima</Button>
    </div>
  </SectionCard>
)
export default HtmlParserPagesTable
