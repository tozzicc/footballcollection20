type ProgressBarProps = {
  value: number
  max?: number
  label?: string
  showPercentage?: boolean
  ariaLabel?: string
}

const ProgressBar = ({
  value,
  max = 100,
  label,
  showPercentage = true,
  ariaLabel,
}: ProgressBarProps) => {
  const percentage = Math.min((value / max) * 100, 100)

  return (
    <div className="progress-container">
      {label && <p className="progress-label">{label}</p>}
      <div
        className="progress-bar-wrapper"
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-label={ariaLabel}
      >
        <div className="progress-bar-fill" style={{ width: `${percentage}%` }} />
      </div>
      {showPercentage && <p className="progress-text">{Math.round(percentage)}%</p>}
    </div>
  )
}

export default ProgressBar
