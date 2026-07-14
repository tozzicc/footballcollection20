import { useState } from 'react'
import WorkspaceCard from '../components/workspace/WorkspaceCard'
import WorkspaceForm from '../components/workspace/WorkspaceForm'
import WorkspaceInfoPanel from '../components/workspace/WorkspaceInfo'
import ConfirmDialog from '../components/ui/ConfirmDialog'
import useWorkspace from '../hooks/useWorkspace'
import { workspaceInfoMock } from '../data/workspaceMock'
import SectionCard from '../components/ui/SectionCard'
import type { WorkspaceStatus } from '../types/workspace'

const statusLabelMap: Record<WorkspaceStatus, string> = {
  unconfigured: 'Ainda não configurado',
  configured: 'Configurado',
}

const WorkspacePage = () => {
  const [confirmClearOpen, setConfirmClearOpen] = useState(false)
  const {
    workspacePath,
    workspace,
    status,
    isConfigured,
    lastUpdated,
    feedbackMessage,
    feedbackType,
    setWorkspacePath,
    saveWorkspace,
    clearWorkspace,
  } = useWorkspace()

  const formattedLastUpdated = lastUpdated
    ? new Date(lastUpdated).toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    : 'Nenhuma atualização ainda.'

  return (
    <div className="page-base">
      <header className="page-header">
        <h1>Workspace</h1>
        <p className="page-subtitle">Configure onde está localizado o acervo do Football Collection.</p>
      </header>

      <div className="workspace-layout">
        <div className="workspace-main">
          <WorkspaceCard
            title="Workspace"
            description="Defina o caminho raiz do acervo utilizado pelo Builder"
          >
            <WorkspaceForm
              workspacePath={workspacePath}
              onPathChange={setWorkspacePath}
              onSave={saveWorkspace}
              onClear={() => setConfirmClearOpen(true)}
              feedbackMessage={feedbackMessage}
              feedbackType={feedbackType}
            />

            <SectionCard title="Workspace Atual" description="Status do caminho configurado">
              <p className="workspace-current-status">{statusLabelMap[status]}</p>
              {isConfigured ? (
                <p className="workspace-saved-path">{workspace.path}</p>
              ) : (
                <p className="workspace-current-status-description">Configure o caminho para começar.</p>
              )}
            </SectionCard>
          </WorkspaceCard>
        </div>

        <aside className="workspace-panel">
          <WorkspaceInfoPanel
            info={workspaceInfoMock}
            status={status}
            lastUpdated={formattedLastUpdated}
          />
        </aside>
      </div>

      <ConfirmDialog
        open={confirmClearOpen}
        title="Limpar Workspace"
        description="Você tem certeza que deseja limpar a configuração do Workspace? Essa ação não poderá ser desfeita."
        confirmLabel="Sim, limpar"
        cancelLabel="Cancelar"
        onConfirm={() => {
          clearWorkspace()
          setConfirmClearOpen(false)
        }}
        onCancel={() => setConfirmClearOpen(false)}
      />
    </div>
  )
}

export default WorkspacePage
