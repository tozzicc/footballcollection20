# Football Collection Builder

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
## Documentação adicional

- Design system: `docs/design-system.md`
- Backend: `backend/README.md`

## Licença

(A ser definida)

## Autor

Football Collection Builder Team
