# Roadmap

## ET-018A — implementada

Correção funcional da primeira versão visual: imagens reais, temporada histórica e descrição estruturalmente associada. A separação semântica de `competition` permanece conservadora e só será preenchida quando houver regra comprovadamente inequívoca.

## ET-018 — implementada

Primeira experiência visual navegável do Football Collection 2.0, separada do Builder e baseada somente na Public API e Media Layer. Ainda não representa um layout final aprovado ou uma versão pronta para produção. Deploy, domínio, CDN, thumbnails, SEO completo, analytics, autenticação e edição permanecem fora do escopo.

## ET-017 — concluída

A camada serve imagens originais de forma controlada e não destrutiva. Permanecem fora do escopo: thumbnails, redimensionamento, conversão, CDN, edição do acervo e publicação do site final.

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

## ET-016 — concluída

Contrato e dados do futuro site público preparados. A ET-016 não implementa layout final, homepage pública, Media Server, thumbnails, SEO, deploy ou edição do catálogo.

## ET-015 — concluída

Normalização editorial não destrutiva, histórica e auditável. Não identifica atributos semânticos das camisas. Permanecem para etapas futuras: temporada, fabricante, jogador, número, competição, versão, home/away, match worn, match issued, descrição editorial e identificação visual. Não usa OCR, IA, internet ou conhecimento externo.

## ET-014 — concluída

Revisão manual assistida por overlays e stable keys reconciliáveis. Criação livre de entidades, merge, edição do acervo e aplicação global dos overlays no CatalogPage permanecem fora do escopo.
