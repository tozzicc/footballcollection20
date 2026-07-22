import type { LastAnalysis } from '../../types/dashboard'

type LastAnalysisCardProps = {
  analysis: LastAnalysis
}

const LastAnalysisCard = ({ analysis }: LastAnalysisCardProps) => (
  <div className="last-analysis-content">
    {analysis.isMock && (
      <p className="analysis-badge">
        <strong>Dados simulados para demonstração</strong>
      </p>
    )}

    <div className="analysis-item">
      <p className="analysis-label">Arquivos processados</p>
      <p className="analysis-value">{analysis.filesProcessed.toLocaleString('pt-BR')}</p>
    </div>

    <div className="analysis-item">
      <p className="analysis-label">Duração da análise</p>
      <p className="analysis-value">{analysis.duration}</p>
    </div>

    <div className="analysis-item">
      <p className="analysis-label">Data e hora</p>
      <p className="analysis-value analysis-date">{analysis.date}</p>
    </div>

    <div className="analysis-status">
      <p className="analysis-label">Status</p>
      <span
        className={`badge badge-${analysis.status === 'success' ? 'success' : 'warning'}`}
      >
        {analysis.status === 'success' ? 'Concluída' : 'Atenção'}
      </span>
    </div>
  </div>
)

export default LastAnalysisCard
