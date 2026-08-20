# Roadmap

## ET-026C — implementada

Semântica final da busca por identidade: equipe exata retorna somente a entidade; múltiplas equipes compatíveis retornam somente equipes; ausência de identidade mantém a busca textual global.

## ET-026B — implementada

Busca contextual concluída: identidade exata de equipe prevalece sobre coincidência textual e restringe resultados pelo vínculo real `countrySlug/teamSlug`. Consultas genéricas permanecem globais, sem alterações no catálogo, banco ou interface.

## ET-026A — implementada

Busca pública refinada com ranking determinístico por identidade e pertencimento, aliases normalizados e contexto da equipe real nos resultados de conteúdo. Resultados secundários permanecem pesquisáveis, sem ocultação, redesign, backend ou rebuild de camadas derivadas.

## ET-026 — implementada

Correções cirúrgicas pós-homologação na busca pública e na representação dos oito registros sem mídia. A busca reutiliza a autoridade editorial existente e inclui o memorial do Chicão; ausências de mídia são declaradas sem ocultação. A divergência atual de 351 coleções vazias e os vínculos que exigem rebuild permanecem adiados, sem iniciar a ET-027.

## ET-020D — implementada

Capas editoriais estáticas e neutras para as três Coleções Históricas e os três grupos de Flâmulas. Os seis assets são exclusivos da interface e não contaminam o domínio histórico ou a Media Layer.

## ET-020C — implementada

Identidade visual própria das Coleções Históricas com covers reais do domínio, cards claros para Brasil/Itália/Outros, imagens integrais sem crop agressivo e microinterações acessíveis exclusivamente em CSS.

## ET-020 — implementada

Domínio complementar para Flâmulas, Bandeiras e Memorabilia, com importação conservadora, runs transacionais, stable keys e slugs determinísticos, Public API própria, Media Layer e páginas públicas responsivas. Catálogo principal, Search, Latest, Hero e Brandings continuam separados.

## ET-018G — implementada

Navegação editorial Equipe → Temporada → Registros, listagem completa de equipes dentro de cada país e padronização global de logos. A experiência moderna preserva a granularidade histórica, as rotas individuais e todas as decisões de Branding e Hero anteriores.

## ET-018F — implementada

Paginação pública real de equipes com 24 registros por página, URL navegável e reset ao alterar busca/filtro. Cards de equipe compactos preservam a escala dos logos históricos, e o footer permanece no fluxo normal sem altura mínima artificial no conteúdo.

## ET-018E — implementada

Identidade histórica de países/seleções separada da mídia editorial por Country Branding derivado e auditável. Brasil e Itália usam os emblemas confirmados nas landings persistidas, “Outros” recebe fallback textual seguro, e a Home passa a organizar o agrupamento como “Bandeiras”, preservando Hero e Team Branding.

## ET-018D — implementada

Identidade de equipes separada da mídia editorial por meio de Team Branding derivado e auditável. Cards públicos usam `logoMedia`, países recebem fallback tipográfico seguro e o Hero passa a compor três imagens locais explicitamente configuradas, sem Latest ou fontes externas.

## ET-018C — implementada

Granularidade editorial corrigida com base nos contextos estruturais HX persistidos. Páginas com múltiplos blocos seguros passam a gerar items, rotas, stable keys, descrições e galerias independentes; estruturas ambíguas permanecem preservadas para revisão. O Hero agora utiliza somente mídia local explicitamente configurada e possui fallback tipográfico.

## ET-018B — implementada

Refinamento exclusivamente visual do site público com tokens isolados, base neutra branca/grafite e azul como destaque. O Builder administrativo, os módulos de processamento, o View Model, a Public API, a Media Layer e os dados persistidos permanecem fora do escopo e inalterados.

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

## ET-018H — concluída

Identidade estrutural dos agrupamentos de imagem/descrição persistida no Parser HTML e consumida pelo catálogo. Registros com descrições repetidas e fronteiras DOM distintas são separados deterministicamente, sem heurística por quantidade ou nome de arquivo. Casos ambíguos continuam em revisão e o acervo histórico permanece somente leitura.

## ET-018I — concluída

Refinamento visual da Home pública: Hero compacto, Latest com variante editorial e mídia contida, Bandeiras em escala menor e globo histórico de Outros associado por evidência direta da navegação legada. Parser, catálogo, normalização e agrupamentos editoriais permaneceram inalterados.

## ET-018J — concluída

Correção estrutural da altura efetiva do Hero, com limite desktop de 455 px, tracks do mosaico sem mínimo intrínseco e alturas próprias para layouts empilhados. O subtítulo da marca pública foi atualizado para “COLEÇÃO DE CAMISAS”, sem alterações no backend ou nas camadas derivadas.

## ET-018J.1 — concluída

Calibração final do Hero para 530 px no desktop e 485 px em 1024 px, mantendo a correção estrutural, a composição histórica e os layouts empilhados existentes.

## ET-018J.2 — concluída

Geometria histórica do mosaico restaurada: painel Torino composto por duas metades à esquerda e estádios Delle Alpi/Comunale empilhados à direita. O quarto asset histórico foi incorporado com reconstrução exclusiva da Media Layer.
## ET-021 — Hero editorial da Home

Implementado o novo hero estático do frontend, com composição integral e CTA HTML proporcional sobre a arte. A montagem histórica Torino e seus arquivos originais permanecem preservados, sem reconstrução de Scanner, Inventory, Parser, Catalog, Media Layer ou View Model.
## ET-021A — Capas editoriais de Países e Regiões

Concluída a identidade editorial da listagem `/site/paises` com capas estáticas para Brasil, Itália e Outros, sem substituir Country Branding ou reconstruir qualquer camada derivada.
## ET-021B — Explore o acervo na Home

Concluída a correção conceitual da navegação geográfica da Home: “Explore o acervo” substitui “Bandeiras” e reutiliza as capas editoriais centralizadas de países, sem interferir no domínio de Coleções Históricas.
## ET-022 — Equipes em destaque

Concluído o refinamento editorial dos destaques da Home, preservando identidade real, dados dinâmicos e classificação existente das equipes. `Italy` permanece sem reclassificação para auditoria futura.

A tentativa posterior de ampliar os GIFs históricos foi revertida na ET-022R por pixelização. O padrão final preserva a resolução aparente original; a normalização completa dos nomes permanece planejada para uma etapa futura.
## ET-023 — Global Team Display Names

Concluída a camada editorial global de nomes de equipes, com fonte de verdade única no frontend e auditoria versionável das 175 entidades. Casos ambíguos permanecem explicitamente sinalizados para revisão futura, sem alterar taxonomia ou identidade persistida.
## ET-023A — Correções pontuais de display

Concluída a normalização centralizada dos três nomes de país/região e o ajuste editorial de Atlético-MG, sem alteração de identidade interna, rotas ou layout.
# ET-024C.1 — concluída

- Composição e ritmo vertical da página memorial refinados sem ampliar a fotografia histórica.
- Rótulo memorial padronizado para “Atlético-MG”; conteúdo e arquitetura da ET-024C preservados.

# ET-024C — concluída em estrutura editorial

- `/site/chicao` contém cabeçalho memorial, depoimento integral, amostra segura de imagens confirmadas e registro informativo dos três AVI.
- Conversão/reprodução audiovisual, galeria completa e integração das demais mídias permanecem pendentes para etapas futuras.

# ET-024B.2 — concluída

- Integração visual da homenagem ao Chicão na Home finalizada com o asset atual considerado oficial.
- PNG integral, botão transparente funcional e placeholder `/site/chicao` preservados.
- ET-024C permanece pendente para a página memorial definitiva.

# ET-024B — tecnicamente implementada

- Chamada editorial da homenagem disponível na Home e vinculada a `/site/chicao`.
- ET-024C pendente: página memorial definitiva.
# ET-024D — concluída

Finalização cirúrgica de `/site/chicao` com links comprovados para o acervo e derivados web dos três vídeos históricos. O card Santos permanece deliberadamente sem navegação por não existir associação segura no catálogo atual. AVI originais, Home, resolvers, backend e camadas derivadas foram preservados.
# ET-024D.1 — concluída

Páginas editoriais próprias das camisas do Chicão adicionadas em `/site/chicao/camisas/*`, priorizando os conjuntos documentais de imagens antes dos dados históricos compactos. Rotas genéricas, vídeos, Home, catálogo e camadas derivadas permanecem intactos; Santos continua fora da navegação por falta de evidência segura.
# ET-024D.1R — concluída

Páginas de camisas do Chicão corrigidas para reutilizar o padrão visual e os dados ordenados dos registros editoriais já existentes no catálogo. O layout específico da ET-024D.1 foi removido; as rotas memoriais e Santos sem link foram preservados.
# ET-024E — concluída

Acesso à homenagem adicionado à navegação principal entre Coleções e Últimas inclusões, reutilizando o padrão existente do header em desktop e mobile.

# ET-029G — aplicada com sucesso

Recuperação oficial e coordenada das 698 associações concluída. Catalog permanece no run 10; Normalization 10, View 16 e Media 18 refletem o estado aprovado. Restam 91 coleções vazias fora do escopo e a dívida editorial das 24 cross-team, ambas sem tratamento automático. Próximo gate: homologação visual manual do site antes da publicação; ET-030 não foi iniciada.
