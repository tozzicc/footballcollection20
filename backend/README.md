# Backend do Football Collection Builder

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
