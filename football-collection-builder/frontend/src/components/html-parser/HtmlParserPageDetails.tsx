import Button from '../ui/Button'
import StatusBadge from '../ui/StatusBadge'
import type { HtmlPageDetails } from '../../types/htmlParser'

const HtmlParserPageDetails = ({ value, onClose }: { value: HtmlPageDetails; onClose: () => void }) => (
  <div className="dialog-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose() }}>
    <section className="dialog-panel parser-details" role="dialog" aria-modal="true" aria-labelledby="parser-details-title">
      <div className="parser-details-header"><div><h2 id="parser-details-title">{value.title}</h2><p>{value.relativePath}</p></div>
        <Button onClick={onClose} ariaLabel="Fechar detalhes">Fechar</Button></div>
      <StatusBadge status={value.parseStatus === 'parsed' ? 'success' : 'error'} label={value.parseStatus} />
      {value.metaDescription && <p>{value.metaDescription}</p>}
      <div><h3>Headings</h3><ul>{value.headings.map((h) => <li key={h.position}>H{h.level}: {h.text}</li>)}</ul></div>
      <div><h3>Previa textual</h3><p>{value.textPreview || 'Sem texto visivel.'}</p></div>
      <div><h3>Imagens ({value.imageReferences.length})</h3><ul className="parser-reference-list">
        {value.imageReferences.map((item, index) => <li key={index}>{item.srcOriginal} - {item.status}</li>)}</ul></div>
      <div><h3>Links ({value.linkReferences.length})</h3><ul className="parser-reference-list">
        {value.linkReferences.map((item, index) => <li key={index}>{item.hrefOriginal} - {item.status}</li>)}</ul></div>
    </section>
  </div>
)
export default HtmlParserPageDetails
