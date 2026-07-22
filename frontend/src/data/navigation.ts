import type { NavigationItem } from '../types/navigation'

const navigation: NavigationItem[] = [
  { id: 'dashboard', label: 'Dashboard', path: '/dashboard', description: 'Visão geral do acervo e pipeline' },
  { id: 'workspace', label: 'Workspace', path: '/workspace', description: 'Configuração do caminho raiz do acervo' },
  { id: 'scanner', label: 'Scanner', path: '/scanner', description: 'Leitura e análise do acervo' },
  { id: 'inventory', label: 'Inventory', path: '/inventory', description: 'Estrutura tipada do conteúdo analisado' },
  { id: 'html-parser', label: 'Parser HTML', path: '/parser-html', description: 'Metadados e referências das páginas legadas' },
  { id: 'catalog', label: 'Catálogo', path: '/catalogo', description: 'Consulta de países, equipes e imagens' },
  { id: 'reports', label: 'Relatórios', path: '/relatorios', description: 'Integridade, duplicidades e arquivos órfãos' },
  { id: 'exports', label: 'Exportações', path: '/exportacoes', description: 'Geração de JSON e pacotes de exportação' },
  { id: 'logs', label: 'Logs', path: '/logs', description: 'Histórico de execuções do Builder' },
  { id: 'settings', label: 'Configurações', path: '/configuracoes', description: 'Caminhos, preferências e parâmetros' },
]

export default navigation
