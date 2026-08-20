# ET-031 — Manifesto do pacote de deploy

## Incluir

| Origem | Destino lógico | Arquivos | Bytes observados | Regra |
|---|---|---:|---:|---|
| `frontend/dist/` | web root da release | 24 | 44.402.827 | Gerar novamente com API de produção; publicar todo o diretório |
| `backend/app/` | backend da release | 172 | 1.026.840 | Incluir código Python |
| `backend/requirements.txt` | backend da release | 1 | pequeno | Instalar em venv novo; não copiar venv local |
| `database/football_collection.db` | storage persistente | 1 | 471.461.888 | Copiar após backup e hashes; nunca apagar com release |
| 15.592 `media_assets.relative_path` sob workspace | storage persistente de mídia | 15.592 | 572.102.472 | Preservar árvore relativa e validar existência/tamanho |

Total mínimo aproximado, sem overhead e sem duplicar `frontend/public`: 1.088.994.027 bytes (aprox. 1,014 GiB).

## Não incluir

- `frontend/node_modules`, `frontend/.env`, caches e dist antigo não regenerado.
- `backend/.venv*`, `backend/venv*`, `__pycache__`, `.pytest_cache`, coverage e logs.
- `.git`, `.pull-staging`, arquivos temporários e relatórios de desenvolvimento desnecessários.
- `database/snapshots` antigos e quaisquer bancos temporários.
- `frontend/public` como segunda cópia: seus assets já integram `dist`.
- Workspace histórico bruto: selecionar somente os 15.592 caminhos efetivamente referenciados.

## Verificações do pacote na ET-032

1. Manifestar cada arquivo com caminho relativo, bytes e SHA-256.
2. Confirmar que nenhum caminho escapa da raiz de mídia e que não há colisões case-sensitive/case-insensitive no SO alvo.
3. Confirmar 15.592 arquivos e 572.102.472 bytes de mídia, ou documentar qualquer diferença antes do cutover.
4. Confirmar DB com 471.461.888 bytes, hash do backup pré-deploy e `integrity_check=ok`.
5. Procurar segredos e URLs locais no artefato final sem imprimir valores.

