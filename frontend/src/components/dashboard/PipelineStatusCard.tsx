import StatusBadge from '../ui/StatusBadge'
import ProgressBar from '../ui/ProgressBar'
import type { PipelineStep } from '../../types/dashboard'

type PipelineStatusCardProps = {
  steps: PipelineStep[]
}

const statusLabelMap: Record<string, string> = {
  completed: 'Concluído',
  in_progress: 'Em andamento',
  pending: 'Aguardando',
  paused: 'Pausado',
}

const PipelineStatusCard = ({ steps }: PipelineStatusCardProps) => (
  <div className="pipeline-container">
    <div className="pipeline-list">
      {steps.map((step) => (
        <div key={step.id} className="pipeline-item">
          <div className="pipeline-header">
            <h3 className="pipeline-step-name">{step.name}</h3>
            <StatusBadge
              status={step.status}
              label={statusLabelMap[step.status]}
            />
          </div>
          <p className="pipeline-description">{step.description}</p>
          <ProgressBar
            value={step.progress}
            label={`${step.progress}%`}
            showPercentage={false}
            ariaLabel={`Progresso de ${step.name}`}
          />
        </div>
      ))}
    </div>
  </div>
)

export default PipelineStatusCard
