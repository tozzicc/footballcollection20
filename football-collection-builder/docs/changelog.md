# Changelog

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
