import type { ChangeEvent } from 'react'
import Button from '../ui/Button'

type WorkspaceFormProps = {
  workspacePath: string
  onPathChange: (value: string) => void
  onSave: () => void
  onClear: () => void
  feedbackMessage: string
  feedbackType: 'success' | 'error' | ''
}

const WorkspaceForm = ({
  workspacePath,
  onPathChange,
  onSave,
  onClear,
  feedbackMessage,
  feedbackType,
}: WorkspaceFormProps) => (
  <form className="workspace-form" onSubmit={(event) => { event.preventDefault(); onSave() }}>
    <label className="field-label" htmlFor="workspace-path">
      Caminho do acervo
    </label>
    <input
      id="workspace-path"
      name="workspacePath"
      type="text"
      placeholder="Exemplo: D:\\FootballCollection"
      value={workspacePath}
      onChange={(event: ChangeEvent<HTMLInputElement>) => onPathChange(event.target.value)}
      className="text-field"
      aria-describedby="workspace-feedback"
    />

    <div className="workspace-form-actions">
      <Button type="submit" variant="primary">Salvar Workspace</Button>
      <Button type="button" variant="secondary" onClick={onClear}>Limpar Workspace</Button>
    </div>

    {feedbackMessage ? (
      <p
        id="workspace-feedback"
        className={`workspace-feedback workspace-feedback-${feedbackType}`}
        role="status"
      >
        {feedbackMessage}
      </p>
    ) : null}
  </form>
)

export default WorkspaceForm
