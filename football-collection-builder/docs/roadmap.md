# Roadmap

## Concluído

- ET-001 a ET-007D — fundações, Workspace e Scanner.
- ET-008 — Inventory Builder.
- ET-009 — Inventory Repository e persistência SQLite.
- ET-010 — Parser HTML do acervo legado.
- ET-010A — integração frontend do Parser HTML concluída.
- ET-011 — Image Parser e auditoria física implementados; validação no acervo real depende da disponibilidade do Workspace persistido.

## Arquitetura após a ET-010

`Workspace → Workspace Reader → Scanner → Inventory Builder → Inventory Persistence Service → Inventory Repository → SQLite`

O Scanner continua como único módulo autorizado a percorrer o disco recursivamente. O Parser abre somente as páginas já registradas no Inventory e nunca altera o Workspace.

## Próxima etapa — ET-011

Pendências deliberadamente mantidas fora da ET-010:

- geração de catálogo HTML;
- parser de imagens;
- hashes e detecção de duplicidades;
- correção automática de links;
- thumbnails;
- sincronização incremental;
- exportações;
- Dashboard consumindo o banco.
# ET-012 — concluída

Catalog Builder inicial: estrutura lógica, relações com imagens, inferências, issues, API e interface. Permanecem fora do escopo: edição manual, merge/deduplicação, identificação visual e semântica de camisas, thumbnails, exportação e sincronização incremental.

## ET-013 — concluída

Camada de qualidade, regras seguras, fila de revisão, agrupamentos, resoluções rastreáveis e indicador técnico. Edição/ignore manual, merges e correções aproximadas seguem fora do escopo.

## ET-014 — concluída

Revisão manual assistida por overlays e stable keys reconciliáveis. Criação livre de entidades, merge, edição do acervo e aplicação global dos overlays no CatalogPage permanecem fora do escopo.
