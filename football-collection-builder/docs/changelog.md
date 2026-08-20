# Changelog

## ET-026C — Busca exata retorna somente a equipe

- Identidade exata única agora produz exatamente um resultado do tipo equipe.
- Consultas compatíveis com múltiplas equipes retornam somente as entidades correspondentes, sem itens.
- Chicão permanece como resultado editorial exclusivo; termos sem identidade preservam a pesquisa global.
- Nenhuma interface, CSS, API, backend, banco ou camada derivada foi alterada.

## ET-026B — Busca contextual por entidade

- Consultas com uma equipe exata e inequívoca agora retornam somente a entidade e conteúdo estruturalmente pertencente a ela.
- Correspondências textuais de outras equipes deixam de participar do contexto exato, sem excluir ou alterar registros.
- Pesquisas multi-entidade e genéricas continuam globais; Chicão permanece editorial.
- Nenhum JSX, CSS, backend, banco ou camada derivada foi alterado/reconstruído.

## ET-026A — Ranking e identidade dos resultados da busca

- Ranking passou a separar identidade exata, conteúdo pertencente, identidade parcial e correspondência textual secundária.
- Consultas sem acento usam o display name existente como alias complementar da mesma API.
- Itens e coleções exibem a equipe proprietária no subtítulo, eliminando contradições entre mídia e texto.
- Nenhum resultado foi filtrado, ocultado ou limitado; CSS, backend, banco e camadas derivadas permaneceram inalterados.

## ET-026 — Correções funcionais pós-homologação

- Busca pública integrada aos display names globais das 175 equipes, com normalização de acentos/hífens e deduplicação.
- Memorial do Chicão incluído como resultado editorial próprio em `/site/chicao`.
- Oito registros sem mídia mantidos acessíveis com comunicação transparente do estado.
- Dois vínculos recuperáveis por correção de encoding foram documentados, sem reconstruir camadas protegidas ou criar associações paralelas.
- Inventory, Parser, Catalog, Normalization, View Model, Media Layer, Historical Collections, banco e workspace permaneceram inalterados.

## ET-020D — Static Editorial Covers for Historical Collections

- Seis composições 512×512 do frontend substituem as covers baseadas em itens históricos.
- Home: capas específicas para Flâmulas, Bandeiras e Memorabilia.
- Grupos: capas específicas para Brasil, Itália e Outros em layout vertical uniforme.
- Assets são servidos diretamente por `/assets/collections/*`, sem Media Layer ou alterações no acervo.
- Fallback de capa usa título discreto; cards de itens reais e paginação removida permanecem intactos.

## ET-020C — Historical Collections Visual Identity

- Covers reais e determinísticas substituem os fallbacks da home de Coleções.
- Atalanta, Genoa e luvas de Stefano Tacconi representam Flâmulas, Bandeiras e Memorabilia.
- Brasil, Atalanta e Ajax identificam os três grupos de Flâmulas sem usar Country Branding.
- Cards de grupo agora são claros, responsivos e coerentes com a paleta editorial.
- Microinterações CSS de 200 ms e entrada de 260 ms respeitam `prefers-reduced-motion`.

## ET-020 — Historical Collections

- Domínio versionado e transacional separado para Flâmulas, Bandeiras e Memorabilia.
- Build real: 196 itens e relações; 193 ready, 3 review required e 0 unavailable.
- Media Layer run 17: 15.592 assets disponíveis e 16.618 relações, sem inválidos ou indisponíveis.
- Nova API `/api/public/collections`, área `/site/colecoes`, paginação e administração em `/colecoes-historicas`.
- Search, Latest, Hero, Brandings e counts principais permanecem inalterados.

## ET-018J.4R — Reversão da composição raster do Hero

- ET-018J.4 revertida após reprovação na validação visual manual.
- Restaurada a composição de quatro assets e a geometria responsiva da ET-018J.3.
- Removidos o JPEG consolidado, seu script Pillow e sua configuração exclusiva, sem rebuild da Media Layer.

## ET-018J.2 — Geometria histórica do mosaico

- O Hero passou a representar quatro arquivos físicos em papéis semânticos: `torinoLeft`, `torinoRight`, `delleAlpi` e `comunale`.
- `a.jpg` e `b.jpg` formam o painel Torino sem gap; ele ocupa aproximadamente 65% da largura, com Delle Alpi e Comunale empilhados na coluna restante.
- Em tablet e mobile, Torino permanece dominante acima e os dois estádios ficam lado a lado abaixo.
- Somente a Media Layer foi reconstruída para disponibilizar `index/picture0003.JPG`; altura do Hero e demais áreas públicas foram preservadas.

## ET-018J.1 — Ajuste final de proporção do Hero

- A altura estrutural do Hero foi ajustada de 455 px para 530 px no desktop largo, mantendo o container como autoridade do grid.
- Em 1024 px, o Hero usa 485 px; em 768 px e 390 px, o comportamento empilhado permanece inalterado.
- O título recebeu aumento discreto no limite superior, de 6,2 rem para 6,5 rem.
- Colunas, mosaico, assets, header, estatísticas, Latest, Bandeiras e páginas internas foram preservados.

## ET-018J — Hero Height Fix & Header Subtitle

- A altura desktop do Hero passou de um piso com `min-height` para `height: 455px`, impedindo que o tamanho intrínseco do mosaico expanda a linha do grid.
- Filhos do grid usam `min-height: 0`; o mosaico usa altura limitada, overflow interno e tracks `minmax(0, 1.2fr) / minmax(0, .8fr)`.
- Em 768 px e abaixo, o Hero recupera altura natural e o mosaico usa 360 px; em 390 px, 300 px.
- O subtítulo da marca foi alterado de “Shirt Archive” para “Coleção de camisas”.
- Assets, Latest, Bandeiras, páginas internas, backend e camadas derivadas permaneceram inalterados.

## ET-018I — Home Visual Refinement

- Hero reduzido de 610 px para 455 px no desktop, com título e espaçamentos responsivos mais compactos; os três assets históricos foram preservados.
- Latest ganhou variante visual com mídia em `contain`, altura reduzida e hierarquia editorial mais densa. A primeira mídia editorial permanece como principal; nenhuma classificação por pixels, filename, OCR ou IA foi criada.
- Cards de Bandeiras passaram a usar área gráfica de 180 px e símbolos limitados a 130 px no desktop.
- O globo histórico `camisas/bandeiras/planeta03.gif`, comprovado nas navegações `paises*.htm`, foi associado a Outros pela regra `CB002_HISTORICAL_OTHERS_NAVIGATION_GLOBE`.
- Somente Country Branding, View Model e Media Layer foram reconstruídos; o contrato público permanece em `1.4.0`.

## ET-018H — Fronteiras editoriais estruturais

- O Parser HTML passou a persistir a identidade estrutural local dos contêineres de imagem e descrição, seus índices no DOM, ordem e chave de grupo determinística.
- Descrições idênticas em blocos HX001 distintos deixam de fundir registros editoriais e suas mídias.
- Estruturas ambíguas continuam sem separação automática; blocos sem descrição permanecem sem legenda inferida.
- Parser HTML, Catalog Builder, Quality, Normalization, View Model e Media Layer foram reconstruídos com histórico preservado.
- As chaves estáveis foram comparadas entre dois builds equivalentes, sem divergências; o schema público permanece em `1.4.0`.

## ET-018G — Country Team Listing & Editorial Season Pages

- Country Pages passaram a mostrar todas as equipes em um grid único, sem paginação visual.
- `/site/equipes` preserva a paginação real criada na ET-018F.
- Identidades de equipe e país usam variantes globais compact/header com escala limitada e `contain`.
- Team Page passou a organizar registros por `seasonLabel`, separando itens sem temporada segura.
- Nova Season Page apresenta um bloco independente por registro, com descrição e mídias exclusivas na ordem persistida.
- Endpoint público mínimo de temporada foi adicionado sem rebuild do View Model ou Media Layer.

## ET-018F — Paginação das Equipes e Compactação dos Cards

- Páginas de país passaram a buscar equipes pelo endpoint paginado, em lotes de 24.
- Listagem geral e páginas de país preservam a página em `?page=N`; busca e filtro reiniciam na página 1.
- Controles informam página, intervalo e total, desabilitando navegação nos limites.
- Cards de equipe e fallbacks foram compactados sem modificar ou ampliar fisicamente os logos históricos.
- Layout vertical corrigido para manter o footer no fluxo sem o espaço artificial causado por `min-height:70vh`.

## ET-018E — Country Branding & Public Home Refinement

- Country Branding versionado com a regra estrutural `CB001` e estados auditáveis.
- Brasil e Itália receberam suas identidades históricas; “Outros” permanece explicitamente indisponível.
- View Model 1.4.0 ampliado com `logoMedia` de países, separado de `primaryMedia`.
- Cards e detalhe de país deixaram de usar iniciais circulares; a Home agora apresenta “Bandeiras”.
- Hero e Team Branding foram preservados sem alteração de regras ou assets.

## ET-018D — Team Branding & Public Hero Composition

- Team Branding versionado com regra estrutural `TB001`, stable keys e estados `matched`, `unavailable` e `ambiguous`.
- View Model 1.3.0 ampliado com `logoMedia`, preservando `primaryMedia` editorial separadamente.
- Cards e cabeçalhos de equipe passaram a usar exclusivamente logos com enquadramento `contain` e fallback neutro.
- Cabeçalhos e cards de país deixaram de promover mídia aleatória de equipes.
- Hero transformado em mosaico responsivo de três imagens configuradas da entrada histórica `meindex.htm`.
- Logos e imagens do Hero continuam servidos pela Media Layer com cache, ETag e Last-Modified.

## ET-018C — registros editoriais e Hero configurado

- Causa do agrupamento corrigida no Catalog Builder: uma página pode produzir múltiplos registros editoriais seguros.
- Grupos contíguos HX `matched` passaram a persistir âncora DOM, status, regra e descrição próprios.
- Stable keys de item passaram a incorporar página e âncora estrutural quando existe mais de um registro.
- Galerias e descrições agora acompanham exclusivamente o registro editorial correspondente.
- View Model atualizado para 1.2.0 e camadas derivadas reconstruídas de forma versionada.
- Hero desacoplado de Latest e configurado explicitamente com `index/picture0004.jpg`, da página histórica `meindex.htm`.
- Fallback do Hero tornou-se exclusivamente tipográfico, sem asset aleatório ou fallback FC.

## ET-018B — refinamento da identidade visual pública

- Paleta bege/creme/mostarda substituída por branco, grafite e azul profundo no site público.
- Tokens CSS semânticos centralizados e isolados sob `.public-site`, sem impacto no Builder.
- Header, busca, hero, estatísticas, cards, fallbacks, breadcrumbs, filtros, paginação, galeria, estados e footer refinados.
- Breakpoints revisados para 1024, 768 e 390 px, preservando o limite de conteúdo em 1440 px.
- Public API, Media Layer, View Model e regras editoriais da ET-018A mantidos sem alteração.

## ET-018A — imagens e camada editorial

- Correção centralizada de `mediaUrl` relativa usando a base configurada da API.
- Contexto estrutural por imagem no Parser HTML, com associação conservadora e auditável.
- Temporadas determinísticas derivadas somente de títulos e filenames históricos.
- Períodos `MM_AA[_lote]` removidos da apresentação editorial pública.
- Home, Latest, equipe, item e galeria adaptados para items, temporadas e descrições seguras.

## ET-018 — Primeira versão visual navegável

- Área pública isolada do AppShell administrativo em `/site`.
- Home editorial com hero real, resumo, últimas inclusões, países e equipes em destaque.
- Navegação por países, equipes, collections e os dois formatos de item.
- Galeria baseada em `mediaUrl`, busca pública, paginação, breadcrumbs e 404 própria.
- Tema visual de arquivo esportivo responsivo e acessível, sem dados técnicos internos.

## ET-017 — Media Layer

- Camada histórica e transacional de assets derivada do View Model e do Parser de Imagens.
- `mediaKey` SHA-256 determinístico, resolver com contenção de caminho e entrega somente leitura.
- API de status, build, resumo, listagem, metadata e conteúdo com cache HTTP e MIME explícito.
- SVG auditável, porém bloqueado inline; nenhum thumbnail, cópia ou alteração do acervo.
- Public API enriquecida com `mediaUrl` e previews reais em `/midia-site` e `/modelo-publico`.

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

## ET-016 — Catalog View Model

- View Model versionado e histórico separado da normalização.
- Public API paginada para entidades, detalhes, navegação, busca e últimas inclusões.
- Rotas de item inequívocas, mídia lógica e página administrativa `/modelo-publico`.

## ET-015 — Catalog Entity Normalization & Enrichment

- Camada normalizada histórica, transacional e separada do catálogo-base.
- Registry de regras v1.0.1, slugs determinísticos por escopo, eventos e overlay manual `matched`.
- API paginada, detalhes, interface `/normalizacao-catalogo` e testes de rollback/reconciliação.

## ET-014 — Revisão Manual Assistida

- Stable keys para country, team, collection, item e issue, com reconciliação segura entre builds.
- Fila manual com preview, decisões tipadas, candidatos, overlay, reversão e histórico imutável.
- Página `/revisao-catalogo` e API completa de revisão.
## ET-021 — Novo hero editorial da Home

- Substituída visualmente a montagem Torino pelo asset editorial estático `football-collection-hero-v2.png` na Home pública.
- Removidos do hero os textos HTML que duplicavam o conteúdo da nova arte.
- Mantido um link HTML real, acessível e responsivo para `/site/paises` sobre a região visual de “Explorar o acervo”.
- Preservados o bloco dinâmico de estatísticas, os assets históricos anteriores e todas as camadas derivadas existentes.
## ET-021A — Capas editoriais de Países e Regiões

- Os cards de Brasil, Itália e Outros em `/site/paises` receberam capas editoriais estáticas associadas por slug.
- Mantidos títulos, contagens dinâmicas, área integralmente clicável, rotas existentes e fallback discreto.
- A alteração não afeta os logos nos detalhes de país, a seção da Home, o backend ou as camadas derivadas.
## ET-021B — Explore o acervo na Home

- Corrigido o título “Bandeiras” para “Explore o acervo” na seção geográfica da Home.
- Os cards Brasil, Itália e Outros passaram a reutilizar a configuração e as capas editoriais da ET-021A.
- Preservados os destinos individuais, o link “Ver todos” para `/site/paises`, as contagens dinâmicas e a coleção histórica Bandeiras.
## ET-022 — Refinamento editorial de Equipes em destaque

- Ampliada a presença visual dos escudos reais exclusivamente nos cards de destaque da Home.
- Correção pós-validação: removido o dimensionamento intrínseco `auto` dos GIFs; a mídia passou de 200 para 165 px e cada logo usa uma caixa proporcional de até 150×140 px.
- O grid específico mantém quatro cards por linha no desktop, dois em tablet e um em mobile.
- ET-022R: a ampliação não foi aprovada por degradar GIFs históricos de baixa resolução e foi revertida. A decisão final prioriza nitidez: mídia de 140 px, dimensões intrínsecas e limite de 100×100 px, preservando nomes editoriais, grid e interação.
- Refinadas hierarquia tipográfica, espaçamento, fallback e microinteração, sem alterar os cards das listagens internas.
- Mantidas seleção dinâmica por quantidade de itens, contagens, links, logos do acervo e a classificação existente `Italy`.
- Nenhuma arte artificial ou imagem externa foi introduzida.
## ET-023 — Global Team Display Names

- Criado resolvedor frontend único e determinístico para nomes editoriais de equipes em todo o site público.
- Preservados nomes internos, slugs, URLs, stable keys, logos e dados persistidos.
- Auditadas 175 equipes: 169 `SAFE`, 6 `AMBIGUOUS`, 0 `REVIEW_REQUIRED`.
- Adicionados testes de acentos, hífens, preposições, fallback, case-insensitive, determinismo e preservação de rota.
- Nenhuma camada derivada foi reconstruída.
## ET-023A — Correções pontuais de nomes de exibição

- Centralizados os displays `Brasil`, `Itália` e `Outros` em helper único, preservando slugs e URLs.
- Alterado exclusivamente o override `brasil/atletico` para “Atlético-MG”.
- Preservados os seis casos ambíguos da ET-023 e todo o estado visual aprovado.
# ET-024C.1 — Refinamento visual da página memorial

- Reduzida a coluna documental do hero e mantida a fotografia de entrada no tamanho natural máximo de 118×252 px.
- Refinados somente os espaços verticais da página memorial para melhorar a continuidade editorial.
- Alterado apenas o rótulo local “Atlético Mineiro” para “Atlético-MG”.
- Preservados depoimento, imagens, AVI, Home e todas as camadas existentes.

# ET-024C — Página memorial “Chicão — O Deus da Raça”

- Substituído o placeholder de `/site/chicao` por uma página editorial definitiva em estrutura.
- Preservados integralmente o depoimento histórico e a autoria de Mauro Matta.
- Integradas cinco imagens confirmadas por cópias estáticas byte a byte, sem alteração dos originais e sem rebuild da Media Layer.
- Registrada a existência dos três AVI sem player, conversão ou alteração.
- Preservada integralmente a chamada memorial aprovada na Home.

# ET-024B.2 — Finalização visual da homenagem na Home

- Consolidado como oficial o PNG atual `chicao-memorial-home.png`, utilizado integralmente e sem transformação.
- Validada a ausência de textos HTML visíveis sobrepostos e preservado o botão transparente proporcional para `/site/chicao`.
- Mantido o placeholder atual; a página memorial completa continua pendente para a ET-024C.

# ET-024B.1 — Correção da sobreposição da arte memorial

- Removida a camada HTML visual duplicada da chamada “Chicão — O Deus da Raça”.
- Mantido um link HTML transparente, proporcional e acessível sobre o botão desenhado no PNG aprovado.
- Preservados o asset, a rota `/site/chicao` e o placeholder da futura ET-024C.

# ET-024B — Chamada editorial “Chicão — O Deus da Raça” na Home

- Adicionada seção documental permanente após “Equipes em destaque”.
- Integrado sem modificação o asset aprovado `chicao-memorial-home.png`.
- Registrada a rota `/site/chicao` com placeholder mínimo; o memorial completo permanece pendente para a ET-024C.
- Preservadas as áreas e camadas aprovadas nas ET-020B a ET-023A.
# ET-024D — Links do acervo e vídeos históricos

- Removida somente a legenda abaixo da fotografia histórica do hero memorial.
- Cards de São Paulo, Seleção Brasileira e Atlético-MG vinculados a itens públicos comprovados pelas mesmas mídias citadas em `chicao/camisas.htm`; Santos permanece sem link por falta de evidência segura.
- Três cópias derivadas MP4 H.264/AAC adicionadas em `frontend/public/assets/chicao/videos`, preservando resolução, proporção e frame rate dos AVI originais.
- O bloco provisório de audiovisual foi substituído por três players HTML5 locais com `controls` e `preload="metadata"`.
# ET-024D.1 — Páginas memoriais das camisas do Chicão

- Criado o namespace editorial `/site/chicao/camisas/*`, sem alterar as páginas genéricas do catálogo.
- São Paulo apresenta `3850.JPG` e `3851.JPG`; Seleção Brasileira apresenta `3845.JPG`, `3844.JPG` e `0001.jpg`; Atlético-MG apresenta `coppa012.jpg` e `coppa013.jpg`, sempre na ordem do HTML histórico.
- Imagens adicionais presentes nos itens genéricos não foram incorporadas por não pertencerem aos mesmos blocos de `chicao/camisas.htm`.
- Os três links do memorial agora apontam às páginas editoriais próprias; Santos permanece sem navegação.
# ET-024D.1R — Reutilização do padrão existente das camisas

- Extraído o bloco visual já usado em `PublicSeasonPage` para `PublicEditorialRecord`, sem alterar sua marcação ou suas classes CSS.
- As páginas `/site/chicao/camisas/*` agora reutilizam diretamente esse componente e a ordem integral de mídias dos itens existentes.
- Removidos o cabeçalho memorial gigante, legendas por imagem, tabela documental e todo o CSS exclusivo introduzido pela ET-024D.1.
- São Paulo 1977 volta a exibir `3850.JPG`, `3851.JPG` e `chicao77.jpg`, conforme o registro existente.
# ET-024E — Homenagem no menu principal

- Adicionado o link “Homenagem” para `/site/chicao` no array central de navegação pública.
- Preservada a ordem: Início, Países, Equipes, Coleções, Homenagem e Últimas inclusões.
- Active state, menu mobile, foco e apresentação reutilizam integralmente o comportamento existente, sem CSS específico.

# ET-029G — Aplicação coordenada oficial

- Aplicadas 698/698 reassociações autorizadas, sem incluir os cinco `fot_gio`, 536 extras ou 217 mistos.
- Recuperadas 260 coleções; vazias reduzidas de 351 para 91, sem esvaziar coleção previamente preenchida.
- Restauradas 16.245 relações Catalog e criados Normalization 10, View 16 e Media 18.
- Preservados 4.465 itens, 8 sem mídia, 15.592 assets, Historical Collections 1 e 24 cross-team preexistentes.
- Criado snapshot integral validado para rollback; testes, HTTP, integridade e FK aprovados.
