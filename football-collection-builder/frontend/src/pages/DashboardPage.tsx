import SectionCard from '../components/ui/SectionCard'
import MetricCard from '../components/dashboard/MetricCard'
import PipelineStatusCard from '../components/dashboard/PipelineStatusCard'
import CountryDistributionCard from '../components/dashboard/CountryDistributionCard'
import LastAnalysisCard from '../components/dashboard/LastAnalysisCard'
import CollectionStatusCard from '../components/dashboard/CollectionStatusCard'
import QuickActionsCard from '../components/dashboard/QuickActionsCard'
import dashboardMock from '../data/dashboardMock'

const DashboardPage = () => (
  <div className="dashboard-page">
    {/* Header */}
    <section className="dashboard-header">
      <h1>Dashboard</h1>
      <p className="dashboard-subtitle">Visão geral do acervo e do pipeline do Builder</p>
    </section>

    {/* Metrics Grid */}
    <section className="metrics-section">
      <div className="metrics-grid">
        {dashboardMock.metrics.map((metric) => (
          <MetricCard key={metric.id} metric={metric} />
        ))}
      </div>
    </section>

    {/* Main Content: Two Columns */}
    <div className="dashboard-main-grid">
      {/* Left Column: Larger */}
      <div className="dashboard-column-left">
        {/* Pipeline Status */}
        <SectionCard
          title="Pipeline"
          description="Etapas do processamento de dados"
        >
          <PipelineStatusCard steps={dashboardMock.pipelineSteps} />
        </SectionCard>

        {/* Country Distribution */}
        <SectionCard
          title="Distribuição por região"
          description="Imagens por grupo geográfico"
        >
          <CountryDistributionCard countries={dashboardMock.countryDistribution} />
        </SectionCard>
      </div>

      {/* Right Column: Smaller */}
      <div className="dashboard-column-right">
        {/* Last Analysis */}
        <SectionCard
          title="Última análise"
          description="Dados simulados para demonstração"
        >
          <LastAnalysisCard analysis={dashboardMock.lastAnalysis} />
        </SectionCard>

        {/* Collection Status */}
        <SectionCard
          title="Status do acervo"
          description="Integridade e configuração"
        >
          <CollectionStatusCard status={dashboardMock.collectionStatus} />
        </SectionCard>

        {/* Quick Actions */}
        <SectionCard
          title="Ações rápidas"
          description="Acesso às principais operações"
        >
          <QuickActionsCard actions={dashboardMock.quickActions} />
        </SectionCard>
      </div>
    </div>
  </div>
)

export default DashboardPage
