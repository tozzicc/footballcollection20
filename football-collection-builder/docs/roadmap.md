# Roadmap

## Concluído

- ET-001 a ET-007D — fundações, Workspace e Scanner.
- ET-008 — Inventory Builder.
- ET-009 — Inventory Repository e persistência SQLite.
- ET-010 — Parser HTML do acervo legado.

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
