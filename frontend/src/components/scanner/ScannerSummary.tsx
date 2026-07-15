import type { ScannerResponse } from '../../types/scanner'
import SectionCard from '../ui/SectionCard'

type ScannerSummaryProps = {
  result: ScannerResponse
}

const formatBytes = (value: number) => {
  if (value < 1024) return `${value} B`
  const units = ['KB', 'MB', 'GB', 'TB']
  let size = value / 1024
  let index = 0
  while (size >= 1024 && index < units.length - 1) {
    size /= 1024
    index += 1
  }
  return `${size.toFixed(size >= 10 || size < 100 ? 0 : 1)} ${units[index]}`
}

const formatDuration = (durationMs: number) => {
  if (durationMs < 1000) return `${durationMs} ms`
  return `${(durationMs / 1000).toFixed(2)} s`
}

const ScannerSummary = ({ result }: ScannerSummaryProps) => (
  <SectionCard title="Resumo da análise" description="Contagens reais obtidas no acervo.">
    <div className="scanner-summary-grid">
      <div className="card-surface">
        <p className="panel-description">Arquivos encontrados: {result.totalFiles}</p>
        <p className="panel-description">Diretórios encontrados: {result.totalDirectories}</p>
        <p className="panel-description">Tamanho total: {formatBytes(result.totalBytes)}</p>
        <p className="panel-description">Duração: {formatDuration(result.durationMs)}</p>
        <p className="panel-description">Início: {result.startedAt}</p>
        <p className="panel-description">Fim: {result.finishedAt}</p>
        <p className="panel-description">Erros não fatais: {result.errors.length}</p>
      </div>
      <div className="card-surface">
        <p className="panel-description">Imagens: {result.categories.images}</p>
        <p className="panel-description">Páginas: {result.categories.pages}</p>
        <p className="panel-description">Dados: {result.categories.data}</p>
        <p className="panel-description">Vídeos: {result.categories.videos}</p>
        <p className="panel-description">Áudios: {result.categories.audio}</p>
        <p className="panel-description">Documentos: {result.categories.documents}</p>
        <p className="panel-description">Compactados: {result.categories.archives}</p>
        <p className="panel-description">Outros: {result.categories.other}</p>
      </div>
    </div>
  </SectionCard>
)

export default ScannerSummary
