# Football Collection Builder

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
