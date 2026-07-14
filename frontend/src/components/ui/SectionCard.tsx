import type { ReactNode } from 'react'

type SectionCardProps = {
  title: string
  description?: string
  children: ReactNode
  className?: string
}

const SectionCard = ({ title, description, children, className = '' }: SectionCardProps) => (
  <section className={`section-card ${className}`.trim()}>
    <div className="section-header">
      <h2 className="section-title">{title}</h2>
      {description && <p className="section-description">{description}</p>}
    </div>
    <div className="section-content">{children}</div>
  </section>
)

export default SectionCard
