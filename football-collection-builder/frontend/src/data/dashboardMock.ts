import type { DashboardData } from '../types/dashboard'

const dashboardMock: DashboardData = {
  metrics: [
    {
      id: 'files-processed',
      label: 'Arquivos processados',
      value: '19.406',
      description: 'Total de arquivos analisados na coleção',
      indicator: 'positive',
    },
    {
      id: 'images-collection',
      label: 'Imagens da coleção',
      value: '16.256',
      description: 'Imagens válidas e catalogadas',
      indicator: 'positive',
    },
    {
      id: 'teams-identified',
      label: 'Equipes identificadas',
      value: '178',
      description: 'Equipes únicas encontradas na coleção',
      indicator: 'neutral',
    },
    {
      id: 'groups-identified',
      label: 'Grupos identificados',
      value: '4',
      description: 'Categorias principais de imagens',
      indicator: 'neutral',
    },
    {
      id: 'ignored-files',
      label: 'Arquivos ignorados',
      value: '687',
      description: 'Arquivos não processados ou inválidos',
      indicator: 'warning',
    },
  ],

  pipelineSteps: [
    {
      id: 'scanner',
      name: 'Scanner',
      status: 'completed',
      description: 'Leitura e classificação inicial de arquivos',
      progress: 100,
    },
    {
      id: 'parser',
      name: 'Parser',
      status: 'in_progress',
      description: 'Análise de metadados e estrutura de arquivos',
      progress: 65,
    },
    {
      id: 'internal-bank',
      name: 'Banco interno',
      status: 'pending',
      description: 'Armazenagem estruturada em sistema local',
      progress: 0,
    },
    {
      id: 'export',
      name: 'Exportação',
      status: 'pending',
      description: 'Geração de relatórios e arquivos para distribuição',
      progress: 0,
    },
  ],

  countryDistribution: [
    { id: 'italy', name: 'Itália', count: 10437 },
    { id: 'brazil', name: 'Brasil', count: 5323 },
    { id: 'others', name: 'Outros', count: 490 },
    { id: 'flags', name: 'Bandeiras', count: 6 },
  ],

  lastAnalysis: {
    isMock: true,
    status: 'success',
    filesProcessed: 19406,
    duration: '2h 34min',
    date: '13 de julho de 2026, 14:32',
  },

  collectionStatus: {
    integrity: 'good',
    validImages: 16256,
    ignoredFiles: 687,
    internalBank: 'not_configured',
  },

  quickActions: [
    {
      id: 'run-analysis',
      label: 'Executar nova análise',
      available: false,
      description: 'Disponível em breve',
    },
    {
      id: 'open-catalog',
      label: 'Abrir catálogo',
      available: false,
      description: 'Disponível em breve',
    },
    {
      id: 'view-reports',
      label: 'Ver relatórios',
      available: false,
      description: 'Disponível em breve',
    },
    {
      id: 'generate-export',
      label: 'Gerar exportação',
      available: false,
      description: 'Disponível em breve',
    },
  ],
}

export default dashboardMock
