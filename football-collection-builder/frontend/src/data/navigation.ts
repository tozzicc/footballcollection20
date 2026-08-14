import type { NavigationItem } from '../types/navigation'

const navigation: NavigationItem[] = [
  { id: 'dashboard', label: 'Dashboard', path: '/dashboard', description: 'Visão geral do acervo e pipeline' },
  { id: 'workspace', label: 'Workspace', path: '/workspace', description: 'Configuração do caminho raiz do acervo' },
  { id: 'scanner', label: 'Scanner', path: '/scanner', description: 'Leitura e análise do acervo' },
  { id: 'inventory', label: 'Inventory', path: '/inventory', description: 'Estrutura tipada do conteúdo analisado' },
  { id: 'html-parser', label: 'Parser HTML', path: '/parser-html', description: 'Metadados e referências das páginas legadas' },
  { id: 'image-parser', label: 'Parser de Imagens', path: '/parser-imagens', description: 'Metadados técnicos e auditoria das imagens' },
  { id: 'catalog', label: 'Catálogo', path: '/catalogo', description: 'Consulta de países, equipes e imagens' },
  { id: 'catalog-quality', label: 'Qualidade do Catálogo', path: '/qualidade-catalogo', description: 'Consistência, ambiguidades e revisão' },
  { id: 'catalog-review', label: 'Revisão do Catálogo', path: '/revisao-catalogo', description: 'Decisões manuais assistidas e rastreáveis' },
  { id: 'catalog-normalization', label: 'Normalização do Catálogo', path: '/normalizacao-catalogo', description: 'Camada editorial não destrutiva do catálogo' },
  { id: 'public-catalog-model', label: 'Modelo do Site', path: '/modelo-publico', description: 'Contrato de apresentação do futuro site público' },
  { id: 'media-layer', label: 'Mídia do Site', path: '/midia-site', description: 'Acesso seguro e somente leitura às imagens' },
  { id: 'public-site', label: 'Abrir primeira versão do site', path: '/site', description: 'Experiência pública navegável do Football Collection 2.0' },
  { id: 'reports', label: 'Relatórios', path: '/relatorios', description: 'Integridade, duplicidades e arquivos órfãos' },
  { id: 'exports', label: 'Exportações', path: '/exportacoes', description: 'Geração de JSON e pacotes de exportação' },
  { id: 'logs', label: 'Logs', path: '/logs', description: 'Histórico de execuções do Builder' },
  { id: 'settings', label: 'Configurações', path: '/configuracoes', description: 'Caminhos, preferências e parâmetros' },
]

export default navigation
