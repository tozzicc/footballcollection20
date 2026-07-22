import type { WorkspaceInfo, WorkspaceStatus, WorkspaceValidationResponse } from '../../types/workspace'
import SectionCard from '../ui/SectionCard'
import StatusBadge from '../ui/StatusBadge'

type WorkspaceInfoProps = {
  info: WorkspaceInfo
  status: WorkspaceStatus
  lastUpdated: string
  validationResult: WorkspaceValidationResponse | null
  validationError: string
  isValidating: boolean
  lastValidatedAt: string
}

const WorkspaceInfoPanel = ({
  info,
  status,
  lastUpdated,
  validationResult,
  validationError,
  isValidating,
  lastValidatedAt,
}: WorkspaceInfoProps) => {
  const physicalStatusLabel = isValidating
    ? 'Validando...'
    : validationResult
      ? validationResult.valid
        ? 'Válido'
        : 'Inválido'
      : validationError
        ? 'Indisponível'
        : 'Ainda não validado'

  const physicalStatusVariant = isValidating
    ? 'info'
    : validationResult
      ? validationResult.valid
        ? 'success'
        : 'error'
      : validationError
        ? 'error'
        : 'warning'

  const normalizedPath = validationResult?.normalizedPath ?? ''
  const validationMessage = validationError
    ? 'Não foi possível conectar ao serviço do Builder. Verifique se o backend está em execução.'
    : validationResult?.message ?? 'Nenhuma validação realizada.'

  return (
    <SectionCard title="Objetivo do Workspace" description={info.objective}>
      <div className="workspace-info-header">
        <p>Status</p>
        <StatusBadge
          status={status === 'configured' ? 'success' : 'warning'}
          label={status === 'configured' ? 'Configurado' : 'Não configurado'}
        />
      </div>

      <div className="workspace-info-physical-status">
        <p>Status de validação física</p>
        <StatusBadge status={physicalStatusVariant} label={physicalStatusLabel} />
      </div>

      <p className="workspace-info-description">{info.description}</p>

      {normalizedPath ? (
        <div className="workspace-info-meta">
          <p className="workspace-info-meta-label">Caminho normalizado</p>
          <p className="workspace-info-meta-value">{normalizedPath}</p>
        </div>
      ) : null}

      <div className="workspace-info-meta">
        <p className="workspace-info-meta-label">Mensagem de validação</p>
        <p className="workspace-info-meta-value">{validationMessage}</p>
      </div>

      <div className="workspace-info-meta">
        <p className="workspace-info-meta-label">Última validação</p>
        <p className="workspace-info-meta-value">{lastValidatedAt}</p>
      </div>

      <div className="workspace-info-meta">
        <p className="workspace-info-meta-label">Última atualização</p>
        <p className="workspace-info-meta-value">{lastUpdated}</p>
      </div>

      <div className="workspace-example">
        <p className="workspace-example-label">Exemplo de estrutura</p>
        <ul className="workspace-example-list">
          {info.exampleStructure.map((item) => (
            <li key={item} className="workspace-example-item">
              {item}
            </li>
          ))}
        </ul>
      </div>
    </SectionCard>
  )
}

export default WorkspaceInfoPanel
