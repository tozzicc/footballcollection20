# Changelog

## ET-011 — Image Parser

- Auditoria somente leitura de JPEG, PNG, GIF, BMP, WebP, TIFF e SVG com Pillow.
- Metadados técnicos, validação, animação, dimensões, DPI e relação com referências HTML persistidos em SQLite.
- Oito endpoints e página `/parser-imagens` com resumo, filtros, paginação e detalhes.
- Consultas de imagens não referenciadas, imagens inválidas e referências quebradas.

## ET-010A — Integração frontend do Parser HTML

- Placeholder de `/parser-html` substituído pela interface funcional.
- Status, execução, atualização, resumo, páginas paginadas, detalhes e referências ausentes integrados aos seis endpoints existentes.
- Timeout de até dez minutos aplicado somente à execução do parser.
- Estados sem Inventory, sem execução anterior, carregamento e erros tratados na página.

## ET-010 — Parser HTML do acervo legado

- BeautifulSoup 4 adicionada com html.parser, sem lxml.
- Parser somente leitura para HTML, HTM e ASP persistidos no Inventory.
- Extração de metadata, headings, prévia textual, imagens e links.
- Resolução tipada de referências internas, ausentes, externas, anchors e itens ignorados.
- Fallback controlado de encoding e tolerância a HTML legado malformado.
- Seis tabelas SQLite, índices, substituição transacional e rollback.
- Seis endpoints e página /parser-html com paginação real e detalhes.
- Testes temporários de parsing, encoding, integridade, persistência e rollback.

## ET-009 — Inventory Repository

- Persistência SQLite adicionada sem ORM.
- Banco `database/football_collection.db` e schema criados automaticamente.
- Seis tabelas e índices para caminho relativo, extensão, categoria e diretório.
- Gravação completa em transação única, com rollback em falhas.
- Inventory Repository, Inventory Persistence Service e cinco endpoints adicionados.
- Página Inventory ampliada com ação de salvar, confirmação e status do banco.
- Testes de criação, schema, persistência, rollback, consultas e regravação adicionados.
## ET-008 — Inventory Builder

- Scanner ampliado de forma retrocompatível com listas tipadas de arquivos e pastas.
- Metadados coletados pelo Workspace Reader na mesma passagem recursiva.
- Inventory Builder implementado sem acesso adicional ao disco.
- Modelos Pydantic de Inventory, itens, pastas, estatísticas, categorias, extensões e metadata.
- Inventory Service e `POST /api/inventory/build` adicionados.
- Página Inventory, serviço, hook, componentes e navegação adicionados ao frontend.
- Tabelas limitadas a 50 registros, responsivas e com rolagem horizontal interna.
- Testes de Scanner e Inventory adicionados; Dashboard mantido com mocks.
# ET-012 — Catalog Builder

- Catálogo transacional persistido em oito tabelas, com inferências e issues rastreáveis.
- API completa de status, build, resumo, países, equipes, items e issues.
- Página Catálogo funcional com busca, filtro, paginação e detalhes.
- Reconhecimento explícito de `MM_AA[_lote]` como período de inclusão.

## ET-013 — Qualidade do Catálogo

- Quality runs, assessments e resolutions transacionais.
- Regras determinísticas CQ001–CQ003, agrupamentos, score, filtros e detalhes.
- Página `/qualidade-catalogo`, sem edição manual ou alteração do acervo.

## ET-014 — Revisão Manual Assistida

- Stable keys para country, team, collection, item e issue, com reconciliação segura entre builds.
- Fila manual com preview, decisões tipadas, candidatos, overlay, reversão e histórico imutável.
- Página `/revisao-catalogo` e API completa de revisão.
