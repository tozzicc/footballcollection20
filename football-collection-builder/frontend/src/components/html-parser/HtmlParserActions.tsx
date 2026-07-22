import Button from '../ui/Button'

type Props = { disabled: boolean; isParsing: boolean; onRun: () => void; onRefresh: () => void }
const HtmlParserActions = ({ disabled, isParsing, onRun, onRefresh }: Props) => (
  <div className="parser-actions">
    <Button variant="primary" disabled={disabled || isParsing} onClick={onRun}>
      {isParsing ? 'Analisando paginas...' : 'Executar Parser HTML'}
    </Button>
    <Button disabled={isParsing} onClick={onRefresh}>Atualizar resultados</Button>
    {isParsing && <span role="status">Analisando paginas em modo somente leitura...</span>}
  </div>
)
export default HtmlParserActions
