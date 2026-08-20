# Football Collection Builder

## Correções funcionais pós-homologação — ET-026

A busca pública reconhece os nomes editoriais globais das equipes com ou sem acentos, preserva os resultados do catálogo e inclui a homenagem ao Chicão como conteúdo editorial. Registros históricos sem mídia permanecem acessíveis e exibem um aviso explícito, sem esconder falhas nem criar associações paralelas. O diagnóstico completo está em `docs/et-026-functional-fixes-report.md`; as coleções vazias continuam reservadas à ET-027.

A ET-026A acrescentou ranking determinístico por identidade e pertencimento. Uma equipe exata aparece antes de seu conteúdo, e este aparece antes de correspondências textuais de outras equipes. Itens preservam o título histórico, mas agora informam explicitamente sua equipe real. Consultas sem acento reutilizam o display name como alias da mesma API, sem backend ou índice paralelo.

A ET-026B tornou essa resolução contextual: quando uma única equipe é identificada exatamente, somente a entidade e conteúdos vinculados estruturalmente a ela participam do resultado. Consultas amplas, como `América` e `1988`, continuam globais. Nenhum registro histórico foi alterado ou ocultado fora do contexto exato.

A ET-026C simplificou o contexto exato: uma equipe identificada inequivocamente agora é o único resultado. Termos compatíveis com várias equipes, como `América`, retornam somente essas entidades; consultas sem identidade, como `1988` e `Brasil`, mantêm a busca global.

## Página memorial “Chicão — O Deus da Raça” — ET-024C

`/site/chicao` apresenta a página memorial editorial baseada no HTML histórico original `chicao/chicao.htm`. O depoimento integral e sua autoria, Mauro Matta, foram preservados sem reescrita. Cinco imagens confirmadas foram copiadas byte a byte para `public/assets/chicao` como ponte frontend estática, sem modificar o acervo original ou reconstruir a Media Layer.

A página utiliza uma imagem histórica de entrada e quatro imagens rotuladas no HTML original como São Paulo, Seleção Brasileira, Santos e Atlético Mineiro. Os três AVI permanecem intactos e são apenas documentados; reprodução e conversão continuam pendentes. A chamada aprovada da Home não foi alterada.

A ET-024C.1 refinou exclusivamente a composição do hero e os espaços verticais da página: a fotografia de entrada permanece limitada aos 118×252 px originais, enquanto o texto ganhou maior protagonismo. O rótulo local da quarta imagem passou a “Atlético-MG”, sem alteração do arquivo ou dos resolvedores globais.

A ET-024D concluiu a integração pública do memorial: removeu a legenda documental do hero, vinculou somente os cards com associação comprovada no catálogo (São Paulo 1977, Seleção Brasileira 1978 e Atlético-MG 1979) e manteve Santos sem link por ausência de item inequivocamente relacionado ao Chicão. Os três AVI históricos permanecem intocados no workspace; derivados MP4 H.264/AAC locais, sem upscale, alimentam os players HTML5 da seção “Registro audiovisual”.

A ET-024D.1 criou destinos editoriais exclusivos em `/site/chicao/camisas/*`. A correção ET-024D.1R passou essas páginas a reutilizar diretamente o mesmo componente e o mesmo conjunto ordenado de mídias dos registros editoriais das páginas de temporada. São Paulo 1977 apresenta frente, costas e jogador; Seleção Brasileira 1978 e Atlético-MG 1979 exibem todas as mídias de seus respectivos registros. Santos continua sem link.

A ET-024E adicionou “Homenagem” à navegação pública principal, entre “Coleções” e “Últimas inclusões”, apontando para `/site/chicao`. O item reutiliza integralmente o `NavLink` e o comportamento responsivo já existentes, incluindo active state nas subrotas do memorial.

## Chamada editorial da homenagem ao Chicão — ET-024B

A Home pública inclui, após “Equipes em destaque”, uma seção documental para “Chicão — O Deus da Raça”, usando exclusivamente o asset estático aprovado `public/assets/collections/chicao-memorial-home.png`. A chamada aponta para `/site/chicao`, que nesta etapa contém apenas um placeholder acessível; a página memorial definitiva permanece reservada à ET-024C.

A ET-024B.2 consolidou a versão atual desse asset como oficial. A imagem permanece integral, proporcional e sem textos HTML visíveis sobrepostos; somente uma área de link transparente, acessível e responsiva acompanha o botão desenhado no PNG. O placeholder de `/site/chicao` permanece inalterado.

## Capas editoriais estáticas — ET-020D

As seis capas da Home de Coleções e dos grupos de Flâmulas são assets visuais próprios do frontend em `public/assets/collections`. Elas não pertencem ao Workspace histórico, não são itens do acervo e não entram em Scanner, Inventory, Image Metadata ou Media Layer. A configuração usa URLs públicas estáticas e mantém os itens internos ligados às mídias históricas reais.

Os cards de capa compartilham imagem acima, texto abaixo, `object-fit: cover`, hover discreto de 200 ms e fallback textual neutro. Os cards de itens históricos continuam usando `object-fit: contain`.

## Identidade Visual das Coleções Históricas — ET-020C

A home de Coleções usa covers explícitas de itens `ready` do próprio domínio: Atalanta para Flâmulas, bandeira física do Genoa para Bandeiras e luvas de Stefano Tacconi para Memorabilia. Os grupos de Flâmulas usam Brasil, Atalanta e Ajax, cada qual pertencente ao grupo correspondente. A configuração guarda apenas slugs determinísticos em `historicalCollectionIdentity.ts`; nenhuma URL física ou imagem externa é usada.

Cards claros, imagens com `object-fit: contain`, hover de 200 ms e entrada discreta de 260 ms preservam o caráter editorial. `prefers-reduced-motion` remove animações e transforms, e nenhuma informação depende de hover.

## Coleções Históricas — ET-020

`/colecoes-historicas` constrói um domínio complementar versionado para Flâmulas, Bandeiras e Memorabilia, sem reutilizar entidades `catalog_*`. O schema `1.0.0` preserva runs, seções, itens e relações de mídia nas tabelas `historical_collection_*`; stable keys usam SHA-256 de seção, HTML de origem, ordem estrutural e referência da imagem. Slugs combinam legenda normalizada e sufixo determinístico.

A área pública começa em `/site/colecoes`. A API fica sob `/api/public/collections`, com summary, seções e itens paginados em lotes de 24. Os 196 assets editoriais entram na Media Layer normal como origem `historical_collection`; imagens órfãs permanecem excluídas. Search, Latest e counts da Home continuam exclusivos do catálogo de camisas.

## Country Team Listing & Editorial Season Pages — ET-018G

As páginas de país carregam todas as equipes por um helper central que percorre a paginação segura da API; os controles visuais foram removidos apenas desse contexto, enquanto `/site/equipes` continua paginada. Team e Country Branding compartilham variantes compactas e de cabeçalho, sempre com `contain` e limites de escala coerentes.

A navegação principal de equipe agora é Equipe → Temporada → Registros editoriais. A rota `/site/paises/{country}/equipes/{team}/temporadas/{season}` apresenta cada item persistido como bloco independente, preservando ordem, descrição e mídias próprias. Rotas individuais de item e collection continuam compatíveis.

## Paginação das equipes e cards compactos — ET-018F

A listagem da página de país era truncada porque renderizava somente as 12 equipes incluídas no payload resumido do detalhe, sem solicitar as páginas seguintes. Países e listagem geral agora consultam `/teams` com `limit=24` e `offset` real, preservam a página em `?page=N` e retornam à página 1 quando busca ou filtro muda.

`PublicTeamCard` usa uma composição compacta, com área de mídia de aproximadamente 140 px e logo limitado a 100×100 px por dimensões automáticas e `object-fit: contain`. O layout público passou a usar flex vertical com `main` flexível, removendo o `min-height` artificial que ampliava o vazio antes do footer.

## Country Branding e refino da Home — ET-018E

A camada derivada Country Branding identifica a imagem editorial que antecede a grade dimensionada de escudos na landing direta de cada país. A regra auditável `CB001_COUNTRY_LANDING_HEADER_LOGO` usa stable keys e persiste os estados `matched`, `unavailable` ou `ambiguous`; não usa filename como evidência e não inventa identidade quando a estrutura não é segura.

O View Model 1.4.0 publica `logoMedia` de países separadamente de `primaryMedia`. Brasil usa `logos/selecaob.gif`, Itália usa `logos/italy2.gif` e “Outros” mantém fallback textual discreto. A Home apresenta a seção “Bandeiras”; a composição aprovada do Hero permanece inalterada.

## Team Branding e composição do Hero — ET-018D

A camada derivada Team Branding identifica logos exclusivamente quando a página estrutural da equipe (`paises/{país}/{equipe}/{equipe}.htm[l]`) referencia um único asset persistido no diretório lógico `logos/`. A regra `TB001_TEAM_LANDING_LOGOS_DIRECTORY` é auditável, usa a stable key da equipe e produz os estados `matched`, `unavailable` ou `ambiguous`; ausência e ambiguidade nunca promovem camisas ou fotografias como fallback.

O View Model 1.3.0 expõe `logoMedia` separadamente de `primaryMedia`. Cards e cabeçalhos de equipe usam somente o logo, com `object-fit: contain`, enquanto países/regiões utilizam identidade tipográfica neutra em vez de herdar mídia de uma equipe.

O Hero público usa uma composição configurável formada por `index/picture0004.jpg`, `index/a.jpg` e `index/b.jpg`, todos referenciados pela entrada histórica `meindex.htm`. Cada asset é entregue pela Media Layer e pode falhar independentemente; nenhuma alternativa de Latest é selecionada.

## Registros editoriais e Hero — ET-018C

O Catalog Builder promove grupos contíguos de `html_image_contexts` com status `matched` a registros editoriais independentes. A separação exige que todas as imagens da página possuam contexto estrutural seguro e utiliza transições de bloco HX, container e posição DOM; quantidade de imagens, filename e nomes de jogadores não participam da regra. Estruturas ambíguas ou não suportadas permanecem agregadas e auditáveis.

Cada registro persiste `editorial_anchor`, status, regra e descrição. Sua stable key combina a entidade pai, a página original e a âncora estrutural, mantendo determinismo entre rebuilds e distinguindo registros editoriais da mesma temporada. O View Model 1.2.0 preserva uma rota e uma galeria por registro.

O Hero deixou de consumir automaticamente a primeira mídia de Latest. Sua mídia é declarada em `publicSiteConfig` e servida pela Media Layer; a configuração atual usa `index/picture0004.jpg` (455×273), originada da composição histórica de `meindex.htm`. Na ausência ou falha dessa mídia, o Hero permanece tipográfico, sem selecionar outro asset.

## Identidade visual pública — ET-018B

O site público em `/site` utiliza uma identidade de arquivo/museu esportivo baseada em branco (`#FFFFFF`), grafite (`#0D1117`) e azuis (`#173B57`, `#275D81` e `#3D85B9`). Os tokens semânticos ficam isolados em `frontend/src/public/styles/public-site.css`, sob `.public-site`, sem alterar a paleta nem os componentes do Builder administrativo.

A nova identidade cobre header, busca, hero, estatísticas, cards, fallbacks, breadcrumbs, filtros, paginação, galeria, estados e footer de todas as rotas públicas. A ET é exclusivamente visual: Public API, Media Layer, View Model 1.1.0, regras editoriais da ET-018A e dados persistidos permanecem inalterados.

## Correção funcional — ET-018A

As URLs relativas da Media Layer agora são resolvidas centralmente com `VITE_API_BASE_URL`, evitando que o navegador solicite imagens ao servidor Vite. A camada editorial pública separa temporada de período interno de inclusão: `MM_AA` e `MM_AA_lote` nunca são apresentados como temporada ou título.

O Parser HTML dirigido persiste contexto estrutural por imagem em `html_image_contexts`. Apenas texto ligado por estruturas DOM observadas recebe status `matched`; blocos compartilhados permanecem `ambiguous`. O View Model 1.1.0 expõe `seasonLabel` e `description` quando seguros. `competition` permanece nulo quando o texto associado não permite uma separação sem interpretação editorial.

## Public Site — ET-018

A primeira versão visual navegável do Football Collection 2.0 está disponível em `/site`. Ela usa um `PublicLayout` próprio, separado do Builder, e consome exclusivamente a Public API e as URLs seguras da Media Layer. Inclui Home, países, equipes, collections, items, galeria, busca, últimas inclusões, breadcrumbs, estados de loading/empty/error e 404 pública.

As rotas de item preservam os dois formatos inequívocos da ET-016 sob o namespace de desenvolvimento `/site`. O layout é responsivo para desktop, tablet e mobile, possui menu colapsável, foco visível, HTML semântico e fallback de imagem. Esta é uma primeira proposta visual: não representa o layout final aprovado nem uma versão pronta para produção.

## Media Layer — ET-017

A rota administrativa `/midia-site` prepara e audita a entrega segura das imagens originais. O build consome somente o último View Model e os metadados persistidos pelo Parser de Imagens, não cria cópias ou thumbnails e não altera o Workspace. Cada asset recebe `mediaKey` SHA-256 determinístico do caminho relativo normalizado.

O endpoint `/api/media/assets/{mediaKey}` resolve o arquivo dentro do Workspace em modo somente leitura, bloqueia traversal e escapes por symlink, valida extensão e contenção, e entrega JPEG, PNG, GIF, BMP, WebP e TIFF com MIME explícito, ETag, Last-Modified e cache público de uma hora. SVG possui metadata, mas é bloqueado para exibição inline. Caminhos físicos, stable keys e IDs SQL não são expostos.

## Visão geral

Football Collection Builder é uma aplicação web para organizar e analisar acervos digitais relacionados a futebol. Ao final da ET-007D, o projeto possui interface navegável, configuração local de Workspace e um Scanner integrado ao backend para leitura recursiva do acervo.

## Status das ETs

- ET-001: concluída
- ET-002: concluída
- ET-003: concluída
- ET-004: concluída
- ET-005: concluída
- ET-006: concluída
- ET-007A: concluída
- ET-007B: concluída
- ET-007D: concluída
- ET-008: concluída
- ET-009: concluída

## Arquitetura atual

```text
Frontend (React + TypeScript + Vite)
  ├─ Workspace salvo no localStorage
  └─ Scanner Page / scannerService
               │ POST /api/scanner/scan
               ▼
Backend (Python + FastAPI)
  ├─ rota e modelos do Scanner
  ├─ Scanner Service
  ├─ Workspace Service (normalização e validação)
  └─ Workspace Reader (percurso recursivo somente leitura)
               │
               ▼
Workspace no sistema de arquivos acessível ao backend
```

O frontend usa `VITE_API_BASE_URL` como URL-base da API. Em desenvolvimento, `frontend/.env.example` sugere `http://127.0.0.1:8000`. O CORS do backend aceita o frontend local em `localhost:5173` e `127.0.0.1:5173`.

## Estrutura do projeto

```text
football-collection-builder/
├── frontend/          # Aplicação React, TypeScript e Vite
├── backend/           # API FastAPI e serviços Python
├── database/          # Scripts e arquivos de banco de dados
├── docs/              # Documentação do projeto
├── exports/           # Arquivos exportados
├── logs/              # Logs da aplicação
├── tests/             # Estrutura de testes do projeto
└── README.md
```

## Scanner do acervo — ET-007D

A ET-007D implementou o fluxo real de análise do Workspace, da interface até o sistema de arquivos:

1. O usuário configura um caminho na página Workspace; a configuração fica no `localStorage` do navegador.
2. A página Scanner reutiliza esse caminho e envia `{ "workspacePath": "..." }` ao backend.
3. O backend normaliza e valida existência, tipo e permissão de leitura do caminho.
4. O `WorkspaceReader` percorre arquivos e diretórios recursivamente sem seguir links simbólicos de diretório.
5. O `Scanner Service` calcula contagens, tamanho total, categorias, extensões, duração e erros não fatais.
6. O frontend apresenta o estado da análise, o resumo e a distribuição por extensão.

### Comportamento somente leitura

O Scanner não cria, edita, move, renomeia nem exclui itens do Workspace. Também não gera catálogo, arquivos auxiliares ou conteúdo dentro do acervo. A leitura de metadados serve apenas para obter tipo e tamanho; erros pontuais são registrados no resultado quando possível.

### Categorias e extensões suportadas

As extensões são normalizadas para minúsculas. Arquivos sem extensão e extensões não mapeadas entram em `other`.

| Categoria | Extensões |
|---|---|
| `images` | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`, `.tif`, `.tiff` |
| `pages` | `.htm`, `.html`, `.asp` |
| `data` | `.json`, `.xml`, `.csv`, `.dat` |
| `videos` | `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.mpeg`, `.mpg` |
| `audio` | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg` |
| `documents` | `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.txt`, `.rtf` |
| `archives` | `.zip`, `.rar`, `.7z`, `.tar`, `.gz` |
| `other` | sem extensão ou qualquer extensão não listada |

### Endpoint `POST /api/scanner/scan`

```json
{
  "workspacePath": "C:\\caminho\\do\\acervo"
}
```

A resposta contém status, caminho normalizado, início, fim, duração, totais de arquivos/diretórios/bytes, contagens por categoria, resumo de extensões e erros não fatais. As extensões são ordenadas por quantidade decrescente e depois alfabeticamente.

## Como executar

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

A documentação interativa da API fica em `http://127.0.0.1:8000/docs`.

### Frontend

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

## Testes implementados

A suíte do backend possui 14 testes: um de health, quatro de validação do Workspace e nove do Scanner Service. O Scanner é testado com diretório vazio, subpastas, totais, classificação, extensões em maiúsculas, arquivo sem extensão, caminhos inválidos, ordenação por extensão e timestamps/duração.

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

## Limitações atuais

- A análise é síncrona e não possui progresso percentual, pausa ou cancelamento.
- O frontend aguarda no máximo 300 segundos; acervos grandes podem exceder esse tempo.
- Resultados não são persistidos e nenhum catálogo é gerado.
- O caminho precisa estar visível e legível para o processo do backend.
- Links simbólicos de diretório não são percorridos.
- A classificação usa somente a extensão, não o conteúdo do arquivo.
- Não há teste automatizado específico do endpoint do Scanner nem do fluxo visual do frontend.


## Inventory Builder — ET-008

O Inventory é a fonte de dados estruturada para os próximos módulos. O fluxo atual é `Workspace → Scanner → Inventory Builder`: somente o Scanner percorre o disco, coleta arquivos, pastas e metadados em uma única passagem; o Builder transforma exclusivamente esses arrays tipados, sem reler o Workspace.

- `POST /api/inventory/build` recebe `workspacePath`, executa o Scanner uma vez e retorna o Inventory completo.
- O Inventory contém metadata, estatísticas, pastas, itens, categorias, extensões e erros.
- Cada item recebe ID determinístico e preserva caminhos, nome, extensão, categoria, tamanho, datas e legibilidade fornecidos pelo Scanner.
- A página `/inventory` apresenta resumo, categorias, extensões e amostras de até 50 pastas e arquivos.
- O endpoint existente `POST /api/scanner/scan` permanece retrocompatível; os campos `files` e `folders` foram adicionados sem modificar o resumo anterior.

### Limitações do Inventory

O Inventory pode ser persistido em SQLite pela ET-009. Ainda não há parsers HTML/imagem, catálogo, hash, duplicidades, exportação, sincronização incremental ou paginação.

## Inventory Repository — ET-009

A camada Repository persiste o Inventory atual em `database/football_collection.db` usando `sqlite3` da biblioteca padrão, sem ORM. O banco e o schema são criados automaticamente.

```text
Inventory → Inventory Persistence Service → Inventory Repository → SQLite
```

As tabelas `inventory_metadata`, `inventory_statistics`, `inventory_folders`, `inventory_items`, `inventory_extensions` e `inventory_categories` são substituídas em uma única transação. Uma falha provoca rollback completo, preservando o Inventory anterior. Índices cobrem caminho relativo, extensão, categoria e diretório.

Endpoints:

- `POST /api/inventory/save`: persiste um Inventory completo;
- `GET /api/inventory/status`: informa criação, última gravação e quantidades;
- `GET /api/inventory/statistics`: retorna estatísticas persistidas;
- `GET /api/inventory/extensions`: retorna extensões persistidas;
- `GET /api/inventory/categories`: retorna categorias persistidas.

Na página Inventory, o botão **Salvar Inventory** persiste o resultado construído e o card **Status do Banco** mostra última gravação, arquivos, pastas e duração da operação.

## Parser HTML — ET-010

O fluxo Inventory Repository → HTML Parser Service → HTML Parser Repository → API → Frontend analisa apenas itens persistidos da categoria pages com extensão .htm, .html ou .asp. O módulo usa BeautifulSoup 4 com html.parser; ASP é tratado exclusivamente como HTML estático e nunca é executado.

A leitura tenta BOM, charset declarado, UTF-8, CP1252 e Latin-1. Título, idioma, descrição, headings, prévia textual de até 500 caracteres, imagens e links são persistidos sem armazenar o HTML completo. Referências internas são resolvidas contra o Inventory; URLs externas não são acessadas.

Endpoints: POST /api/html-parser/parse, GET /api/html-parser/status, GET /api/html-parser/summary, GET /api/html-parser/pages, GET /api/html-parser/pages/{id} e GET /api/html-parser/missing-references. A interface está em /parser-html.

O parser é sequencial, síncrono e somente leitura: não corrige links, baixa recursos, executa ASP/JavaScript, cria arquivos ou altera o Workspace.

Na ET-018H, cada contexto de imagem passou a registrar índices dos contêineres de imagem e descrição no DOM, tipos dos contêineres, ordem estrutural e uma chave de grupo local determinística. O Catalog Builder usa essa fronteira para impedir que descrições textualmente iguais fundam registros editoriais distintos; ambiguidades continuam preservadas para revisão.

Na ET-018I, a Home pública recebeu refinamento de proporção: Hero mais compacto, cards Latest com apresentação específica em `contain` e Country Branding em escala reduzida. Latest continua usando a primeira mídia na ordem editorial persistida, sem classificador visual. A identidade de Outros usa o globo histórico `planeta03.gif`, ligado pelas páginas legadas de navegação.

Na ET-018J, o Hero passou a ter altura estrutural efetiva de 455 px no desktop. O ajuste substitui o antigo piso de `min-height`, limita a contribuição intrínseca do mosaico e mantém altura natural nos layouts empilhados. O subtítulo do header público agora é “COLEÇÃO DE CAMISAS”.

Na ET-018J.1, a mesma regra estrutural foi calibrada para 530 px no desktop largo e 485 px em 1024 px, preservando 42,5% para texto e 57,5% para o mosaico. Layouts empilhados, header e demais seções não foram modificados.

Na ET-018J.2, o mosaico recuperou a geometria comprovada em `meindex.htm`: `a.jpg` e `b.jpg` compõem Torino à esquerda; `picture0004.jpg` (Delle Alpi) e `picture0003.JPG` (Comunale) ficam empilhados à direita. A composição usa quatro arquivos físicos em três áreas visuais, sem gerar ou modificar imagens.

A ET-010A concluiu a interface em `/parser-html`, incluindo status, execução e atualização, resumo persistido, paginação e busca de páginas, detalhes e referências ausentes.

## Image Parser — ET-011

O Image Parser consulta exclusivamente as imagens do Inventory persistido e usa Pillow em modo somente leitura para extrair formato, dimensões, proporção, modo, alpha, animação, frames e DPI. SVG é validado sem rasterização. Resultados, erros e execuções são persistidos no SQLite e cruzados com as referências produzidas pelo Parser HTML, sem reler páginas.

Endpoints: `POST /api/image-parser/parse`, `GET /api/image-parser/status`, `GET /api/image-parser/summary`, `GET /api/image-parser/images`, `GET /api/image-parser/images/{id}`, `GET /api/image-parser/orphans`, `GET /api/image-parser/invalid` e `GET /api/image-parser/broken-references`. A interface está em `/parser-imagens`.

O módulo não gera previews ou thumbnails, não extrai EXIF pessoal e não altera, converte, renomeia ou remove arquivos do Workspace.
## Documentação adicional

- Design system: `docs/design-system.md`
- Backend: `backend/README.md`

## Licença

(A ser definida)

## Autor

Football Collection Builder Team

# Catalog Builder (ET-012)

O módulo **Catálogo** transforma exclusivamente os dados persistidos do Inventory, Parser HTML e Parser de Imagens em `Country/Region → Team → Collection → Item → Images`. O build não relê o Workspace e não executa etapas anteriores. Inferências preservam valor original, origem e confiança; ambiguidades ficam em Issues. Pastas `MM_AA` e `MM_AA_lote` são períodos de inclusão (anos 2000), nunca temporadas. Consulte a página `/catalogo` ou os endpoints `/api/catalog/*`.

## Qualidade do Catálogo (ET-013)

`/qualidade-catalogo` analisa issues já persistidos, agrupa padrões e registra avaliações e resoluções rastreáveis sem reler ou alterar o acervo. As regras CQ001–CQ003 exigem evidência estrutural persistida e inequívoca; os demais casos ficam `review_required`.

O Quality Score é apenas um indicador técnico: `100 × (0,75 × entidades classificadas / entidades totais + 0,25 × (1 − pendências / (entidades totais + pendências)))`, limitado a 0–100.

## Revisão Manual Assistida (ET-014)

`/revisao-catalogo` oferece fila, candidatos pesquisáveis, preview sem persistência, resolve, acknowledge, defer, reversão lógica e histórico. Decisões formam overlays; entidades-base e `originalName` nunca são alterados. O autor técnico é `local_user`.

Identidade entre rebuilds usa SHA-256 de composições canônicas persistidas: country=`tipo+caminho`; team=`tipo+stableKey(country)+caminho`; collection=`tipo+stableKey(team)+caminho`; item=`tipo+stableKey(team/collection)+relativePath da página`; issue=`tipo do issue+stableKey(entity)+relativePath+assinatura da mensagem+ordinal determinístico`. Separadores e caixa são canonizados. IDs, timestamps, slugs isolados e conteúdo físico não participam.

## Normalização do Catálogo — ET-015

A rota `/normalizacao-catalogo` cria uma camada editorial histórica e não destrutiva sobre o último Catalog Build. Countries/Regions, Teams, Collections e Items preservam `stableKey`, nomes/títulos e caminhos originais. Nenhum arquivo do Workspace é lido ou alterado.

As regras versionadas `CN001`, `TM001`, `CL001`, `IT001`, `SL001`, `SL002` e `MR001` tratam whitespace/Unicode/HTML entities, casing uppercase seguro, períodos de inclusão, slugs e overlays manuais reconciliados. Os estados são `normalized`, `unchanged`, `review_required` e `overridden`; as fontes são `original`, `deterministic_rule` e `manual_review`. Colisões de slug recebem seis caracteres do SHA-256 da `stableKey` dentro do escopo lógico.

## Catalog View Model — ET-016

A rota administrativa `/modelo-publico` inspeciona o contrato de apresentação preparado para o futuro Football Collection 2.0. O View Model consome somente o último run completo da normalização, possui schema `1.0.0`, runs históricos e Public API paginada sob `/api/public/catalog`.

Items com collection usam `/items/{country}/teams/{team}/collections/{collection}/{item}`; items sem collection usam `/items/{country}/teams/{team}/items/{item}`. As rotas e breadcrumbs são persistidos, não expõem stableKeys/IDs SQL e preservam os slugs da ET-015. Mídia é apenas referência lógica; nenhum arquivo físico é servido.
### ET-021 — Hero editorial da Home

O hero público de `/site` usa agora o asset estático `frontend/public/assets/collections/football-collection-hero-v2.png`, preservado integralmente com dimensionamento proporcional. A chamada “Explorar o acervo” continua sendo um link HTML real e acessível para `/site/paises`, posicionado proporcionalmente sobre o botão representado na arte. A montagem histórica anterior foi preservada nos assets do acervo; nenhuma camada derivada foi reconstruída.
### ET-021A — Capas editoriais de Países e Regiões

A página `/site/paises` associa deterministicamente os slugs `brasil`, `italia` e `outros` a três capas PNG estáticas do frontend. As capas usam preenchimento editorial com `object-fit: cover`, enquanto títulos, contagens e rotas continuam provenientes da aplicação. Logos históricos dos detalhes, backend e camadas derivadas permanecem inalterados.
### ET-021B — Explore o acervo na Home

A seção geográfica da Home deixou de usar a nomenclatura histórica inadequada “Bandeiras” e passou a se chamar “Explore o acervo”. Os atalhos Brasil, Itália e Outros compartilham as capas editoriais da ET-021A, mantêm contagens dinâmicas e apontam para as rotas de país existentes; a coleção histórica Bandeiras permanece independente em `/site/colecoes/bandeiras`.
### ET-022 — Equipes em destaque

Os cards de “Equipes em destaque” da Home mantêm uma variante editorial própria, seleção, ordenação, contagens e rotas dinâmicas. A tentativa de ampliar os pequenos GIFs históricos não foi aprovada devido à pixelização e foi revertida: a mídia usa 140 px e os logos preservam dimensões intrínsecas, limitadas a 100×100 px com `object-fit: contain`. Os nomes mantêm capitalização de display e as correções determinísticas `Atlético` e `Grêmio`; a classificação `Italy` permanece preservada para auditoria futura. A normalização editorial completa dos nomes ficará para uma ET posterior.
### ET-023 — Global Team Display Names

O site público utiliza um resolvedor único de nomes editoriais de equipes em `teamDisplayName.ts`. Slugs, rotas, stable keys e nomes persistidos permanecem intactos; somente a apresentação é normalizada em Home, listagens, país, equipe, temporadas, itens, Latest, busca e breadcrumbs. A auditoria das 175 equipes está em `docs/team-display-names-audit.md`: 169 casos `SAFE`, 6 `AMBIGUOUS` e nenhum `REVIEW_REQUIRED`. A entidade `italia/italy` mantém sua taxonomia e rota, exibindo apenas “Itália”. Nenhuma camada foi reconstruída.
### ET-023A — Correções pontuais de display

Os nomes de país/região agora passam pelo helper centralizado `countryDisplayName`, exibindo `Brasil`, `Itália` e `Outros` sem alterar seus slugs ou rotas. O override global `brasil/atletico` passou de “Atlético Mineiro” para “Atlético-MG”. Layout, logos, ET-022R, seis casos ambíguos e dados persistidos permanecem inalterados.

### ET-029G — Recuperação oficial das associações

Aplicadas oficialmente 698 reassociações de itens para coleções comprovadas. O pipeline coordenado preservou 4.465 itens, recuperou 260 coleções, restaurou 16.245 relações Catalog e gerou Normalization 10, View 16 e Media 18. Permanecem 91 coleções vazias, 8 itens sem mídia, 11 itens `fot_gio` e as 24 anomalias cross-team controladas. O snapshot pré-aplicação e a auditoria completa estão documentados em `docs/et-029g-official-coordinated-apply.md`.
