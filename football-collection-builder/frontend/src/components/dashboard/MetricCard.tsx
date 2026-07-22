import type { Metric } from '../../types/dashboard'

type MetricCardProps = {
  metric: Metric
}

const MetricCard = ({ metric }: MetricCardProps) => (
  <article className="metric-card">
    <div className="metric-content">
      <p className="metric-label">{metric.label}</p>
      <p className="metric-value">{metric.value}</p>
      <p className="metric-description">{metric.description}</p>
    </div>
    {metric.indicator && (
      <div className={`metric-indicator metric-indicator-${metric.indicator}`} />
    )}
  </article>
)

export default MetricCard
