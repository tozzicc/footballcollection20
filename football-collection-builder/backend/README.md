# Backend do Football Collection Builder

## Historical Collections — ET-020

`HistoricalCollectionsService` lê somente os HTMLs autorizados de Pennants, Flags e Memorabilia, preserva a ordem estrutural e persiste um run transacional com schema `1.0.0`. As tabelas são `historical_collection_runs`, `historical_collection_sections`, `historical_collection_items` e `historical_collection_media`.

Admin: `POST /api/historical-collections/build` e `GET /api/historical-collections/status`. API pública: `GET /api/public/collections/summary`, `/sections`, `/sections/{section}`, `/sections/{section}/items` e `/sections/{section}/items/{slug}`. Flâmulas também oferecem `/sections/pennants/groups` e `/groups/{group}`. A paginação padrão é 24 e o contrato não expõe paths, HTML de origem, IDs, stable keys ou regras internas.

A Media Layer consome `historical_collection_media` como fonte explícita e reutiliza o mesmo algoritmo de media key. O build real produziu 196 itens: 148 Flâmulas, 9 Bandeiras e 39 itens de Memorabilia; 193 `ready`, 3 `review_required` e nenhum indisponível.

## ET-018G — consulta pública de temporada

`GET /api/public/catalog/seasons/{country}/{team}/{season}` consulta exclusivamente o View Model corrente e devolve equipe, país, resumo e registros editoriais com suas mídias na ordem persistida. A resposta omite source page, stable keys, caminhos físicos, IDs e regras internas. Nenhuma camada derivada precisa ser reconstruída.

## ET-018E — Country Branding

`CountryBrandingService` deriva identidades a partir da posição editorial do emblema antes da grade de thumbnails na landing direta do país. As tabelas versionadas `country_branding_runs` e `country_branding` registram regra, origem, confiança e status. O View Model 1.4.0 expõe `logoMedia` sem caminhos físicos, stable keys ou IDs internos, e a Media Layer entrega os assets com cache HTTP.

## ET-018D — Team Branding

`TeamBrandingService` deriva logos por stable key usando somente a associação estrutural entre a landing page da equipe e um único asset persistido sob `logos/`. Os resultados versionados ficam em `team_branding_runs` e `team_branding`, com regra, origem, confiança e status auditáveis. O View Model 1.3.0 publica `logoMedia` sem expor stable keys, caminhos físicos ou IDs internos; a Media Layer continua responsável pela entrega HTTP.

## ET-018A — contexto editorial seguro

`html_image_contexts` registra ordem DOM, container, texto associado, regra HX001–HX004, confiança e status. HX001 cobre o padrão legado predominante de uma tabela com o grupo de fotos seguida por uma tabela textual; HX002/HX003 cobrem container único; HX004 bloqueia associação em blocos compartilhados. O parser não usa `text_preview` para essa relação e mantém o Workspace somente leitura.

O View Model 1.1.0 acrescenta campos compatíveis de temporada e descrição. As regras SE001–SE005 aceitam anos e temporadas presentes em título/filename e rejeitam períodos internos de inclusão.

## Media Layer (ET-017)

`MediaService` cria runs históricos e transacionais nas tabelas `media_build_runs`, `media_assets` e `media_asset_relations`. A identidade pública é o SHA-256 do caminho relativo normalizado (Unicode NFC, barras POSIX e case-folding). A API oferece `POST /api/media/build`, `GET /api/media/status`, `/summary`, `/assets`, `/assets/{mediaKey}/metadata` e `/assets/{mediaKey}`.

`MediaResolver` aceita somente chaves hexadecimais de 64 caracteres, rejeita caminhos absolutos, `..`, drive prefixes e escapes do Workspace após `resolve()`. A resposta binária usa MIME derivado do formato validado, ETag, Last-Modified e `Cache-Control: public, max-age=3600`. SVG não é servido inline (415); assets inválidos retornam 422 e ausentes ou inseguros retornam 404. Nenhuma rota retorna caminhos físicos.

API Python construída com FastAPI. Ao final da ET-007D, o backend oferece health check, validação de Workspace e análise recursiva do acervo em modo somente leitura.

## Requisitos

- Python 3.10+
- `venv`

## Instalação e execução

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

A documentação OpenAPI interativa estará disponível em `http://127.0.0.1:8000/docs`.

## Arquitetura do Scanner

- **Rota (`app/api/routes/scanner.py`)**: publica `POST /api/scanner/scan` e aplica os modelos de entrada e saída.
- **Modelos (`app/models/scanner.py`)**: definem o contrato do request, resumo, categorias, extensões e erros.
- **Scanner Service (`app/services/scanner_service.py`)**: coordena validação, leitura, classificação e agregação.
- **Workspace Service (`app/services/workspace_service.py`)**: normaliza o caminho e valida existência, tipo e permissão de leitura.
- **Workspace Reader (`app/services/workspace_reader.py`)**: fornece o iterador recursivo somente leitura e ignora links simbólicos de diretório.

O frontend chama a API por meio de seu `scannerService`, usando `VITE_API_BASE_URL`. O backend permite, via CORS, chamadas do Vite em `localhost:5173` e `127.0.0.1:5173`.

## Endpoint do Scanner

### `POST /api/scanner/scan`

```json
{
  "workspacePath": "C:\\caminho\\do\\workspace"
}
```

Exemplo com PowerShell:

```powershell
$body = @{ workspacePath = 'C:\caminho\do\workspace' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/api/scanner/scan' -ContentType 'application/json' -Body $body
```

Campos retornados:

- `status`, `message` e `workspacePath` normalizado;
- `startedAt`, `finishedAt` e `durationMs`;
- `totalFiles`, `totalDirectories` (inclui a raiz) e `totalBytes`;
- `categories`, com a quantidade de arquivos por categoria;
- `extensions`, com extensão normalizada e quantidade;
- `errors`, com falhas não fatais encontradas durante a leitura.

O resumo de extensões é ordenado por quantidade decrescente e depois alfabeticamente. Extensões são normalizadas para minúsculas.

## Classificação de arquivos

| Categoria | Extensões reconhecidas |
|---|---|
| `images` | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`, `.tif`, `.tiff` |
| `pages` | `.htm`, `.html`, `.asp` |
| `data` | `.json`, `.xml`, `.csv`, `.dat` |
| `videos` | `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.mpeg`, `.mpg` |
| `audio` | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg` |
| `documents` | `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.txt`, `.rtf` |
| `archives` | `.zip`, `.rar`, `.7z`, `.tar`, `.gz` |
| `other` | arquivos sem extensão ou com extensão não mapeada |

## Garantia de somente leitura

O Scanner apenas percorre diretórios e lê metadados necessários para contagem e tamanho. Ele não cria, altera, move, renomeia ou exclui arquivos e diretórios; não muda permissões ou datas; não gera catálogo nem grava dados no Workspace. Links simbólicos de diretório não são seguidos.

Erros pontuais ao acessar um item ou seus metadados são coletados em `errors` quando o percurso pode continuar. Caminhos vazios, inexistentes, sem leitura ou que não sejam diretórios falham na validação antes da análise.

## Testes

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

A suíte inclui 34 testes cobrindo health, Workspace, Scanner, Inventory Builder, Inventory Service, Repository SQLite, schema, rollback, consultas e regravação. Os testes do Scanner verificam diretório vazio, subpastas, totais de arquivos/diretórios/bytes, classificação, extensões em maiúsculas, arquivos sem extensão, caminhos inválidos, ordenação das extensões e timestamps/duração.

## Limitações atuais

- A execução é síncrona; não há fila, progresso percentual, pausa ou cancelamento.
- O resultado não é persistido e nenhum catálogo é criado.
- A duração cresce conforme o tamanho e as condições de acesso do acervo.
- O caminho precisa ser visível e legível pelo processo do backend.
- Links simbólicos de diretório são ignorados.
- A classificação considera somente a extensão, não o conteúdo do arquivo.
- Não há teste automatizado específico para `POST /api/scanner/scan`; a lógica é exercitada diretamente nos testes do Scanner Service.

## Inventory Builder — ET-008

O Inventory Builder transforma a resposta tipada do Scanner sem acessar o sistema de arquivos. O `WorkspaceReader` coleta metadados durante a mesma passagem recursiva do Scanner, que agora inclui `files` e `folders` de forma aditiva e retrocompatível.

### `POST /api/inventory/build`

Request:

```json
{ "workspacePath": "C:\\caminho\\do\\workspace" }
```

A resposta contém:

- `metadata`: geração, versão do Scanner, Workspace e duração;
- `statistics`: totais de arquivos, diretórios, tamanho e categorias previstas;
- `folders` e `items`: representação tipada do acervo;
- `categories` e `extensions`: resumos reutilizáveis;
- `errors`: falhas não fatais herdadas do Scanner.

Arquitetura: a rota delega ao `InventoryService`, que executa o Scanner uma vez e entrega sua resposta ao `Inventory Builder`. O Builder não importa nem utiliza `WorkspaceReader`, `Path` ou APIs de sistema de arquivos.
## Inventory Repository — ET-009

A persistência usa `sqlite3`, sem ORM, no arquivo padrão `database/football_collection.db`. `app/database` gerencia conexão e schema; `InventoryRepository` executa somente operações de banco; `InventoryPersistenceService` valida contagens, delega a gravação e confirma o resultado.

### Schema

- `inventory_metadata`
- `inventory_statistics`
- `inventory_folders`
- `inventory_items`
- `inventory_extensions`
- `inventory_categories`

Todas as tabelas possuem chave primária. Há índices em `relative_path`, `extension`, `category` e `directory`. Não há triggers.

Cada gravação limpa o Inventory anterior e insere metadata, estatísticas, extensões, categorias, pastas e arquivos na mesma transação. Em caso de exceção, é executado rollback.

### Endpoints de persistência

- `POST /api/inventory/save`
- `GET /api/inventory/statistics`
- `GET /api/inventory/extensions`
- `GET /api/inventory/categories`
- `GET /api/inventory/status`

O corpo de `/api/inventory/save` é o modelo `Inventory` completo produzido pelo Builder.

## Parser HTML — ET-010

BeautifulSoup 4 com html.parser extrai metadados e referências de .htm, .html e .asp. A fonte é exclusivamente o Inventory SQLite; não ocorre novo scan. ASP e JavaScript nunca são executados, recursos externos nunca são acessados e o HTML completo não é persistido.

Encodings são tentados nesta ordem: BOM, charset declarado, UTF-8, CP1252 e Latin-1. Caminhos relativos, ../, raiz do site, barras Windows, URL encoding, query string e fragmento são normalizados antes da consulta ao Inventory.

As tabelas são html_parse_runs, html_pages, html_headings, html_image_references, html_link_references e html_parse_errors, com índices para execução, página, item do Inventory, caminho e status. A substituição é transacional e preserva o Inventory.

Endpoints: POST /api/html-parser/parse; GET /api/html-parser/status; GET /api/html-parser/summary; GET /api/html-parser/pages; GET /api/html-parser/pages/{page_id}; GET /api/html-parser/missing-references.

O processamento é sequencial e síncrono. Falhas por página são registradas sem interromper as demais; falhas fatais de persistência provocam rollback.

Desde a ET-018H, `html_image_contexts` também persiste os índices dos contêineres de imagem e descrição, `structural_group_key`, tipos dos contêineres e ordem estrutural. A chave é local à página e identifica a fronteira real do DOM; texto repetido não participa da identidade. HX001–HX003 podem formar grupos seguros, enquanto HX004 e estruturas insuficientes permanecem ambíguas ou não suportadas.

## Image Parser — ET-011

O `ImageParserService` consulta imagens no Inventory, lê metadados com Pillow e persiste resultados via `ImageParserRepository`. SVG é tratado sem Pillow. O cruzamento com HTML reutiliza `referenced_inventory_item_id` e referências ausentes já normalizadas pelo Parser HTML.

As tabelas `image_parse_runs`, `image_metadata` e `image_parse_errors` armazenam execuções, metadados e falhas. Os endpoints ficam sob `/api/image-parser`: `parse`, `status`, `summary`, `images`, `images/{id}`, `orphans`, `invalid` e `broken-references`.
# Catalog Builder

`POST /api/catalog/build` (corpo `{"replacePrevious": true}`) cria uma versão transacional a partir das tabelas já persistidas. Endpoints de leitura: `/api/catalog/status`, `/summary`, `/countries`, `/teams`, `/teams/{id}`, `/items`, `/items/{id}` e `/issues`. Países e equipes são inferidos somente sob a estrutura histórica `paises`; agrupamentos em `camisas/{país}/{equipe}` tornam-se collections. `MM_AA[_lote]` é classificado como `inclusion_period`. O serviço contém regras; o repositório contém schema, transações, filtros, busca e paginação.

Confidence aceita `confirmed`, `inferred` ou `unknown`; source aceita `folder`, `html`, `inventory` ou `manual` (reservado). Não há edição, merge, OCR, IA, deduplicação ou identificação de temporada nesta etapa. O Workspace original é somente leitura.

## Catalog Quality

`POST /api/catalog/quality/analyze` analisa somente o último catálogo persistido. Status, summary, issues, detalhes, resolutions e groups ficam sob `/api/catalog/quality`. Cada issue recebe `auto_resolved` ou `review_required`; `open` e `ignored` permanecem preparados semanticamente. CQ001 valida períodos `MM_AA[_lote]` já classificados; CQ002 valida país já não desconhecido; CQ003 valida equipe ligada a país estrutural não desconhecido. Nenhuma regra altera `originalName`, funde ou exclui entidades.

Score: `100 × (75% da proporção de entidades classificadas + 25% do fator 1 − pendências/(entidades + pendências))`, limitado a 0–100. Ele não representa percentual de correção.

## Manual Catalog Review

Endpoints `/api/catalog/review` fornecem status, summary, fila, detalhe, candidates, preview, resolve, acknowledge, defer, revert e history. Códigos: `MR_ASSIGN_COUNTRY`, `MR_ASSIGN_TEAM`, `MR_ASSIGN_COLLECTION`, `MR_CLASSIFY_FOLDER`, `MR_CONFIRM_MISSING_IMAGE`, `MR_ACKNOWLEDGE` e `MR_DEFER`. Preview valida sem escrever; resolve/revert são transacionais; reversão nunca apaga histórico.

`catalog_stable_keys` separa identidade lógica de IDs AUTOINCREMENT. A composição está documentada no README principal. Rebuild reconcilia por igualdade exata: uma correspondência=`matched`, nenhuma=`orphaned`, múltiplas=`conflict`; somente `matched` pode alimentar overlay. O valor original permanece intacto.

## Catalog Entity Normalization (ET-015)

`CatalogNormalizationService` lê exclusivamente o último catálogo persistido e reviews ativos `resolved` + `matched`. As regras ficam centralizadas em `catalog_normalization_rules.py`; o repository mantém runs históricos, quatro conjuntos de entidades normalizadas e eventos em uma única transação.

Endpoints: status, run, summary, coleções paginadas `countries`, `teams`, `collections`, `items`, detalhes por `stableKey` e events sob `/api/catalog/normalization`. Períodos `MM_AA`/`MM_AA_lote` reutilizam mês, ano e lote validados pelo Builder e nunca representam temporada.

## Catalog View Model / Public API (ET-016)

`CatalogViewService` deriva entidades públicas exclusivamente do último normalization run completo. `CatalogViewRepository` persiste histórico e atende countries, teams, collections, items, media, navigation, search e latest. A versão corrente é `VIEW_SCHEMA_VERSION=1.4.0`.

`ready` indica estrutura navegável, `review_required` preserva pendências da normalização e `unavailable` indica ausência de campos/relacionamentos mínimos. Primary Media prioriza `isPrimaryCandidate`, depois a primeira relação persistida válida; sem relação retorna `null`. A API nunca retorna `absolutePath`, `workspacePath`, stableKey ou IDs SQL.
