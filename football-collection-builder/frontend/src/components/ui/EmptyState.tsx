import type { ReactNode } from 'react'

type EmptyStateProps = {
  title: string
  description?: string
  action?: ReactNode
}

const EmptyState = ({ title, description, action }: EmptyStateProps) => (
  <div className="empty-state">
    <h3 className="empty-title">{title}</h3>
    {description && <p className="empty-description">{description}</p>}
    {action && <div className="empty-action">{action}</div>}
  </div>
)

export default EmptyState
