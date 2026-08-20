# ET-031 — Production readiness e plano de publicação

Data da auditoria: 2026-08-20  
Escopo: auditoria local, preparação e planejamento; nenhum deploy executado.  
Gate: **OPTION_A_READY_FOR_DEPLOY_CONFIGURATION**.

## Resumo executivo

O projeto está tecnicamente pronto para a configuração de deploy. Testes, lint, build, HTTP local e banco passaram. Não há bloqueador técnico desconhecido. A publicação depende de configuração e dados do ambiente: servidor/SO, domínio, acesso, web server e localização/backup do site atual.

A arquitetura recomendada é um único domínio HTTPS: o web server entrega `frontend/dist`, aplica fallback SPA para rotas sem arquivo, encaminha `/api/*` ao FastAPI em loopback e bloqueia externamente endpoints administrativos/de escrita. Isso evita CORS no fluxo público e mantém a porta 8000 interna.

O ponto crítico conhecido é a Media Layer: os 15.592 assets (572.102.472 bytes) não estão no build. Em runtime, o backend combina `media_assets.relative_path` com `inventory_metadata.workspace_path`, atualmente `C:\Users\camilo.tozzi\Desktop\Área de Trabalho\FC\Football Collection`. Logo, produção precisa copiar o subconjunto referenciado preservando caminhos e atualizar controladamente o workspace persistido, ou montar a árvore no caminho configurado. É uma dependência resolvível no deploy, não um bloqueador.

## Arquitetura constatada

### Frontend

- React 19.2.7, React DOM 19.2.7 e React Router DOM 6.30.4; TypeScript 6.0.2.
- Vite 8.1.4 no build executado, com plugin React, Tailwind CSS 4.3.2 e configuração sem `base` explícita; base efetiva `/`.
- Source: `frontend/src`; entrada HTML: `frontend/index.html`; entrada JS: `/src/main.tsx`; router: `frontend/src/app/router.tsx` com `BrowserRouter`.
- Build oficial: `npm run build` (`tsc -b && vite build`); saída: `frontend/dist`.
- Resultado: PASS, 138 módulos; 24 arquivos e 44.402.827 bytes. Principais: `index.html` 0,47 kB, CSS 62,36 kB (gzip 11,31), JS 380,61 kB (gzip 103,64).
- Rotas públicas ficam sob `/site`; o mesmo bundle contém rotas administrativas sob `/dashboard`, `/workspace`, `/scanner` etc. A raiz `/` redireciona hoje a `/dashboard`.
- O web server deve servir arquivos existentes e devolver `index.html` para refresh direto em todas as rotas cliente, inclusive `/site`, `/site/paises`, `/site/equipes`, `/site/colecoes`, `/site/ultimas`, `/site/chicao`, equipes, coleções e itens. `/api/*` deve ser decidido antes do fallback e enviado ao backend.
- Assets estáticos em `frontend/public` são copiados ao `dist`; 21 arquivos, 43.959.379 bytes. Portanto, publicar `dist`, sem duplicar `public`.

### Configuração da API

- `frontend/.env` e `.env.example`: `VITE_API_BASE_URL=http://127.0.0.1:8000` (configuração de desenvolvimento embutida no build atual).
- `ApiClient` e `resolveMediaUrl` usam `VITE_API_BASE_URL`, com fallback para string vazia/same-origin; não há outra URL absoluta de runtime relevante no código do frontend.
- Produção recomendada: build com API same-origin (valor vazio) e reverse proxy `/api/*` para `127.0.0.1:8000`. O build de validação não é o artefato final de publicação porque contém a URL de desenvolvimento.
- Domínio final não foi identificado no projeto e não deve ser inventado.

### Backend

- FastAPI, entrada `backend/app/main.py`, aplicação `app.main:app`, versão declarada `0.1.0-alpha`.
- Desenvolvimento: Uvicorn em `127.0.0.1:8000` (README); produção proposta: ambiente virtual novo a partir de `backend/requirements.txt`, Uvicorn sem reload, bind em loopback e supervisor do SO (systemd, Windows Service ou container, após conhecer o servidor).
- Dependências declaradas: FastAPI, `uvicorn[standard]`, Pydantic, BeautifulSoup4 e Pillow. Versões não estão fixadas: reproduzibilidade deve ser tratada na ET-032 ou em uma ET curta de preparação.
- CORS atual: somente `http://localhost:5173` e `http://127.0.0.1:5173`; métodos GET, POST e OPTIONS; headers `*`; credenciais desativadas. Classificação `CONFIG_REQUIRED`: same-origin elimina a necessidade pública; se houver origem separada, cadastrar somente o domínio HTTPS exato.
- A aplicação expõe GETs públicos, Media Layer e também POSTs/build/review/inventory. Não existe autenticação/autorização constatada. Antes do cutover, o proxy deve permitir publicamente apenas a superfície necessária (GET público, mídia e health), negando rotas administrativas e métodos mutáveis; ou deve existir autenticação equivalente.
- Mídia é entregue por `/api/media/assets/{media_key}` após validação SHA-256, extensão permitida, contenção no workspace e existência do arquivo.
- Logging atual: Uvicorn/stdout e handler genérico Python; não há configuração de arquivo, retenção ou rotação. Produção precisa capturar stdout/stderr pelo supervisor e definir rotação/retenção.

### Banco e persistência

- SQLite em `database/football_collection.db`; caminho calculado de forma relativa ao projeto em `backend/app/database/database.py`.
- Tamanho final: 471.461.888 bytes; SHA-256 observado ao final: `E2A0311F2B01C118E6F5BE67AEC163FAFF37E034AC2948D6881B98DB4D56CD1D`.
- O uso público normal é de leitura, mas o processo expõe rotas que podem criar schema, executar builds, revisões e escritas; assim, o runtime da aplicação é tecnicamente read-write e requer permissão de escrita no diretório para DB, journal e eventual WAL.
- Não há PRAGMA WAL configurado. Não é requisito para a primeira publicação se os endpoints mutáveis forem bloqueados e houver uma única instância; qualquer alteração de journal/workers exige teste específico.
- Manter DB e mídia em diretórios persistentes que não sejam apagados ao trocar releases. Como o caminho do DB é relativo, a ET-032 deve usar um diretório estável `database/` compartilhado/montado na posição esperada, sem alterar o arquivo durante o cutover.

## Assets e dependências absolutas

- Runtime externo relevante: **1 raiz absoluta**, o `inventory_metadata.workspace_path` acima (`RUNTIME_REQUIRED`). Ela resolve 15.592 caminhos relativos; todos os 15.592 arquivos estavam presentes, zero ausente, total físico/registrado 572.102.472 bytes.
- Referências absolutas em documentação, testes, staging legado e inventários são `DOCUMENTATION_ONLY`, `TEST_ONLY`, `DEVELOPMENT_ONLY` ou dados históricos; não constituem dependências executáveis adicionais de produção.
- O pacote precisa de: `frontend/dist`; `backend/app` + requirements; DB oficial; 15.592 mídias selecionadas com árvore relativa preservada. Não é necessário publicar o workspace bruto além desse conjunto.
- Chicão está pronto: imagens de Home e memorial e os MP4 `brasileiro-1977.mp4`, `entrevista-2005.mp4` e `sao-paulo-3x2-santos-1981-chicao-perde-o-bigode.mp4` estão em `frontend/public/assets/chicao`/`assets/collections` e foram copiados ao `dist`. O frontend referencia MP4, não AVI.
- Estimativa mínima sem duplicação: dist 44.402.827 + backend source 1.026.840 + DB 471.461.888 + mídia 572.102.472 = **1.088.994.027 bytes** (aprox. 1,014 GiB / 1,089 GB). Reservar no servidor pelo menos três cópias desse estado (release, backup, rollback), ambiente Python, logs e folga; recomendação operacional mínima de 5 GiB livres, preferencialmente mais.
- Não enviar: `node_modules`, venvs, `.env` de desenvolvimento, `.git`, `.pull-staging`, snapshots antigos, logs, caches, `__pycache__`, `.pytest_cache`, coverage, temporários, DBs auxiliares e `frontend/public` separado quando `dist` já o contém.

## Segurança, Git e infraestrutura

- Busca por termos sensíveis não identificou credencial de produção configurada no código/pacote; ocorrências foram palavras de domínio/teste/documentação. Mesmo assim, `.env` local não deve subir. Nenhum valor secreto é reproduzido aqui.
- Root Git detectado: `C:\`; o projeto não tem repositório próprio e aparece integralmente como não rastreado (`?? ./`) no root amplo. Há alto risco de um commit capturar arquivos fora do projeto. Antes de versionar, criar/validar repositório dedicado na raiz do projeto e revisar o manifesto; nenhum commit/push foi feito.
- Mensagem futura sugerida: `release: prepare Football Collection 2.0 public site`; tag futura sugerida: `v2.0.0`, somente após deploy/homologação.
- Não existem Dockerfile, compose, nginx.conf, web.config, Procfile, unit service ou script de deploy no escopo do projeto.
- Nenhum domínio, HTTPS, DNS, firewall ou web server de produção está configurado no projeto.
- Portas locais: Vite dev 5173; preview de validação 4173; FastAPI 8000. Em produção, apenas 80 (redirect) e 443 devem ser externos; 8000 fica em loopback/rede privada; 5173/4173 não são usadas.
- HTTPS depende de domínio, DNS, servidor/web server e política de certificado ainda não informados.

## Web, cache, performance e SEO

- Cache: JS/CSS têm nomes com hash e podem receber cache longo/imutável. `index.html` deve usar `no-cache` ou revalidação curta. Imagens/MP4 versionados podem ter cache longo; respostas de mídia por chave podem ter cache público controlado após validar cabeçalhos no servidor.
- Gzip/Brotli no proxy é otimização recomendada, não bloqueador.
- Não foi identificado carregamento obrigatório de todo o acervo na Home; o maior volume fica atrás de endpoints/mídias individuais. Não há bloqueador óbvio de performance no bundle principal.
- `index.html` ainda tem `<title>frontend</title>`, idioma `en` e não tem meta description/canonical/social metadata: `PRE_PUBLICATION_REQUIRED` para título/idioma/description mínimos, classificado como `CONFIG_REQUIRED` por exigir pequena correção local antes do artefato final.
- Não existe `robots.txt`; não há `Disallow: /` acidental. Ausência: `POST_V1` (ou criar no cutover quando domínio estiver definido).
- Não existe sitemap; com milhares de URLs, gerar após domínio/canonical: `POST_V1`, não bloqueia deploy técnico.
- Favicon existe (`frontend/public/favicon.svg`) e está referenciado por `/favicon.svg`: `READY`.

## Validação executada

- Backend: `pytest -q` — **134 passed**, 1 warning de depreciação Starlette/httpx, 155,70 s.
- Nomes: **6/6 passed**; busca pública: **11/11 passed**.
- Lint: `npm run lint` — PASS.
- Build: PASS. Uma primeira execução contida falhou com `spawn EPERM` no binário nativo; repetição isolada/autorizada passou em 897 ms, demonstrando limitação do sandbox, não falha do projeto.
- HTTP local: 200 para `/site`, `/site/paises`, `/site/equipes`, `/site/colecoes`, `/site/ultimas` e `/site/chicao`; mídia real retornou 200 `image/jpeg`.
- Banco: `PRAGMA integrity_check = ok`; `foreign_key_check = 0`.
- Baseline: 3 países; 175 equipes; 930 coleções; 4.465 itens; 91 coleções vazias; 8 itens sem mídia; 24 cross-team conhecidos; `fot_gio` 11 (os dois últimos confirmados pela baseline oficial ET-029G/ET-030, sem reexecutar auditoria de 30 mil URLs).

## Matriz de prontidão

| # | Item | Classe |
|---:|---|---|
| 1 | Build reproduzido | READY |
| 2 | Testes backend | READY |
| 3 | Testes frontend | READY |
| 4 | Lint | READY |
| 5 | Integridade/baseline SQLite | READY |
| 6 | Rotas HTTP locais | READY |
| 7 | Fallback SPA compreendido | READY |
| 8 | API e mídia compreendidas | READY |
| 9 | Assets necessários inventariados | READY |
| 10 | Chicão e MP4 no dist | READY |
| 11 | Backup/rollback desenhados | READY |
| 12 | Favicon | READY |
| 13 | Nenhuma credencial de produção identificada | READY |
| 14 | API de produção/same-origin | CONFIG_REQUIRED |
| 15 | CORS de produção | CONFIG_REQUIRED |
| 16 | Copiar mídia e atualizar/montar workspace | CONFIG_REQUIRED |
| 17 | Persistência/ACL do SQLite | CONFIG_REQUIRED |
| 18 | Reverse proxy + fallback | CONFIG_REQUIRED |
| 19 | Bloquear/autenticar superfície administrativa | CONFIG_REQUIRED |
| 20 | Supervisor e logging/rotação | CONFIG_REQUIRED |
| 21 | Build final sem `.env` local | CONFIG_REQUIRED |
| 22 | SEO mínimo (lang/title/description) | CONFIG_REQUIRED |
| 23 | Repositório Git dedicado | CONFIG_REQUIRED |
| 24 | Servidor e sistema operacional | USER_INPUT_REQUIRED |
| 25 | Domínio/DNS/HTTPS | USER_INPUT_REQUIRED |
| 26 | Método de acesso e privilégios | USER_INPUT_REQUIRED |
| 27 | Web server/supervisor existente | USER_INPUT_REQUIRED |
| 28 | Diretório e processo do site atual | USER_INPUT_REQUIRED |
| 29 | Janela de cutover/rollback | USER_INPUT_REQUIRED |
| 30 | robots.txt | POST_V1 |
| 31 | sitemap | POST_V1 |
| 32 | Brotli/gzip e cache avançado | POST_V1 |
| 33 | Pin de dependências/otimizações de performance | POST_V1 |

Contagem: **READY 13; CONFIG_REQUIRED 10; USER_INPUT_REQUIRED 6; BLOCKER 0; POST_V1 4**.

## Plano numerado da ET-032 (não executado)

1. Receber e validar as seis informações do usuário listadas abaixo; escolher implementação compatível com o SO/web server real.
2. Criar diretório de release paralelo e diretórios persistentes separados para DB, mídia, logs e backups; validar espaço e permissões.
3. Parar mutações, executar `PRAGMA integrity_check` e `foreign_key_check`, criar `database/snapshots/et-032-pre-deploy-YYYYMMDD-HHMMSS.db`, registrar bytes e SHA-256 e copiar também a configuração/site atual para rollback.
4. Criar ambiente Python limpo, instalar requirements e executar testes; produzir build frontend final com API same-origin e SEO mínimo corrigido; não levar `.env` local.
5. Copiar DB oficial para a área persistente sem sobrescrever origem; copiar exatamente as 15.592 mídias preservando caminhos; ajustar/montar `workspace_path` controladamente e provar 15.592/15.592 disponíveis.
6. Instalar o backend sob supervisor, sem reload, em loopback:8000; capturar logs com rotação; validar health, catálogo e mídia internamente.
7. Configurar web server para `dist`, fallback SPA, reverse proxy `/api`, limites/métodos públicos, headers/cache e negação/autenticação de rotas administrativas.
8. Configurar domínio, DNS e HTTPS conforme ambiente; manter site antigo ativo enquanto a nova versão é validada em host/URL temporário.
9. Executar smoke pré-cutover: seis páginas, equipe, coleção, item, busca, Chicão/MP4, API e mídias.
10. Fazer cutover atômico de web root/upstream; validar 80→443, certificado, domínio, cache e smoke externo.
11. Abrir gate de observação de logs/erros; se qualquer critério crítico falhar, restaurar web root/config anterior, parar novo backend e recolocar site anterior. Banco antigo nunca é sobrescrito; se houve escrita no novo, preservar para análise antes de restauração.
12. Somente após estabilização: homologação visual pós-publicação, commit/tag e atualização de README/changelog/roadmap em ET própria.

## Informações mínimas necessárias do usuário

1. Servidor de produção e sistema operacional.
2. Domínio final e quem controla DNS/certificado HTTPS.
3. Método de acesso (SSH/RDP/painel) e nível de privilégio disponível.
4. Web server e mecanismo de serviço existentes, se houver.
5. Diretório/configuração do site antigo e procedimento aceito para seu backup.
6. Janela desejada de cutover e tempo máximo aceitável para acionar rollback.

## Integridade de escopo

- Banco não foi alterado; nenhum run, rebuild, migração, snapshot ou restore foi feito.
- Nenhum deploy, cópia externa, DNS, domínio, HTTPS, hospedagem ou firewall foi alterado.
- Nenhum commit ou push foi feito.
- README, changelog, roadmap, frontend e backend permaneceram sem alteração pela ET-031.

