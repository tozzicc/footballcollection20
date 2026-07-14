import type { ReactNode } from 'react'
import SectionCard from '../ui/SectionCard'

type WorkspaceCardProps = {
  title: string
  description: string
  children: ReactNode
}

const WorkspaceCard = ({ title, description, children }: WorkspaceCardProps) => (
  <SectionCard title={title} description={description}>
    {children}
  </SectionCard>
)

export default WorkspaceCard
