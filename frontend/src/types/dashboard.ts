export type Metric = {
  id: string
  label: string
  value: string | number
  description: string
  indicator?: 'positive' | 'neutral' | 'warning'
}

export type PipelineStatus = 'completed' | 'in_progress' | 'pending' | 'paused'

export type PipelineStep = {
  id: string
  name: string
  status: PipelineStatus
  description: string
  progress: number
}

export type CountrySummary = {
  id: string
  name: string
  count: number
}

export type LastAnalysis = {
  isMock: boolean
  status: 'success' | 'warning' | 'error'
  filesProcessed: number
  duration: string
  date: string
}

export type CollectionStatus = {
  integrity: 'good' | 'warning' | 'critical'
  validImages: number
  ignoredFiles: number
  internalBank: 'configured' | 'not_configured'
}

export type QuickAction = {
  id: string
  label: string
  available: boolean
  description?: string
}

export type DashboardData = {
  metrics: Metric[]
  pipelineSteps: PipelineStep[]
  countryDistribution: CountrySummary[]
  lastAnalysis: LastAnalysis
  collectionStatus: CollectionStatus
  quickActions: QuickAction[]
}
