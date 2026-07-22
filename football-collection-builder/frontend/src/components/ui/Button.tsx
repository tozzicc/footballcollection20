import type { ReactNode } from 'react'

type ButtonProps = {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  className?: string
  ariaLabel?: string
}

const Button = ({
  children,
  variant = 'secondary',
  disabled = false,
  onClick,
  type = 'button',
  className = '',
  ariaLabel,
}: ButtonProps) => (
  <button
    type={type}
    className={`btn btn-${variant}${disabled ? ' btn-disabled' : ''} ${className}`.trim()}
    disabled={disabled}
    onClick={onClick}
    aria-label={ariaLabel}
  >
    {children}
  </button>
)

export default Button
