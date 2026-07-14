import Button from '../ui/Button'
import type { QuickAction } from '../../types/dashboard'

type QuickActionsCardProps = {
  actions: QuickAction[]
}

const QuickActionsCard = ({ actions }: QuickActionsCardProps) => (
  <div className="quick-actions-grid">
    {actions.map((action) => (
      <div key={action.id} className="quick-action-wrapper">
        <Button
          disabled={!action.available}
          onClick={() => {
            if (action.available) {
              console.log(`Action triggered: ${action.id}`)
            }
          }}
          className="quick-action-button"
          ariaLabel={action.label}
        >
          <span>{action.label}</span>
        </Button>
        {!action.available && action.description && (
          <p className="quick-action-hint">{action.description}</p>
        )}
      </div>
    ))}
  </div>
)

export default QuickActionsCard
