type StatusBadgeProps = {
  status: 'success' | 'warning' | 'error' | 'info' | 'completed' | 'in_progress' | 'pending' | 'paused'
  label: string
}

const statusColorMap: Record<StatusBadgeProps['status'], string> = {
  success: 'badge-success',
  warning: 'badge-warning',
  error: 'badge-error',
  info: 'badge-info',
  completed: 'badge-success',
  in_progress: 'badge-info',
  pending: 'badge-warning',
  paused: 'badge-warning',
}

const StatusBadge = ({ status, label }: StatusBadgeProps) => (
  <span className={`badge ${statusColorMap[status]}`}>{label}</span>
)

export default StatusBadge
