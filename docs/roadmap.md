# Roadmap

## Concluído

- ET-001 a ET-007D — fundações, Workspace e Scanner.
- ET-008 — Inventory Builder.

## Arquitetura após a ET-008

`Workspace → Workspace Reader → Scanner → Inventory Builder → módulos consumidores`

O Scanner é o único módulo autorizado a percorrer o disco. O Inventory passa a ser a fonte estruturada que módulos futuros deverão consumir.

## Próxima etapa — ET-009

Pendências deliberadamente mantidas fora da ET-008:

- definir persistência do Inventory;
- integrar os próximos consumidores ao Inventory;
- definir processamento especializado de conteúdo conforme a especificação da ET-009;
- manter fora de escopo até autorização: catálogo real, hashes, duplicidades, parsers e exportações.