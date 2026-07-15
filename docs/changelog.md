# Changelog

## ET-008 — Inventory Builder

- Scanner ampliado de forma retrocompatível com listas tipadas de arquivos e pastas.
- Metadados coletados pelo Workspace Reader na mesma passagem recursiva.
- Inventory Builder implementado sem acesso adicional ao disco.
- Modelos Pydantic de Inventory, itens, pastas, estatísticas, categorias, extensões e metadata.
- Inventory Service e `POST /api/inventory/build` adicionados.
- Página Inventory, serviço, hook, componentes e navegação adicionados ao frontend.
- Tabelas limitadas a 50 registros, responsivas e com rolagem horizontal interna.
- Testes de Scanner e Inventory adicionados; Dashboard mantido com mocks.