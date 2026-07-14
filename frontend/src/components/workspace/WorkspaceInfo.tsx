import type { WorkspaceInfo, WorkspaceStatus } from '../../types/workspace'
import SectionCard from '../ui/SectionCard'
import StatusBadge from '../ui/StatusBadge'

type WorkspaceInfoProps = {
  info: WorkspaceInfo
  status: WorkspaceStatus
  lastUpdated: string
}

const WorkspaceInfoPanel = ({ info, status, lastUpdated }: WorkspaceInfoProps) => (
  <SectionCard title="Objetivo do Workspace" description={info.objective}>
    <div className="workspace-info-header">
      <p>Status</p>
      <StatusBadge
        status={status === 'configured' ? 'success' : 'warning'}
        label={status === 'configured' ? 'Configurado' : 'Não configurado'}
      />
    </div>

    <p className="workspace-info-description">{info.description}</p>

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

export default WorkspaceInfoPanel
