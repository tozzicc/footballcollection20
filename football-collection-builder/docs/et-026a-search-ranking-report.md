# ET-026A — Relevância e apresentação da busca pública

## Causa raiz

A ET-026 acrescentava as entidades editoriais antes dos resultados da API, porém preservava a ordem interna da API para todo o conteúdo restante. O backend pesquisa somente `title/name` e `original_title/original_name`; sua classificação considera igualdade/prefixo textual, sem distinguir identidade de equipe de conteúdo. Para “São Paulo”, cinco itens têm `title = São Paulo` e `original_title = SÃO PAULO`, portanto recebiam relevância equivalente.

Na apresentação, o frontend mostrava `title` como título e `originalTitle` como subtítulo. Como os dois campos repetiam “São Paulo”, a equipe proprietária não aparecia. A mídia primária desses registros é o GIF persistido na relação do item — nos quatro casos auditados, o símbolo de sua equipe real — criando contradição visual entre imagem e texto.

## Auditoria do caso São Paulo

| Entidade real | Rota | Campo que casou | Apresentação anterior | Motivo da prioridade | Depois da ET-026A |
|---|---|---|---|---|---|
| Caxias | `/site/items/brasil/teams/caxias/items/sao-paulo` | `title = São Paulo`; `original_title = SÃO PAULO` | `Item / São Paulo / SÃO PAULO` | igualdade exata na API, sem peso de pertencimento | após o item do próprio São Paulo; subtítulo `Equipe: Caxias` |
| Chapecoense | `/site/items/brasil/teams/chapecoense/items/sao-paulo` | mesmos campos | `Item / São Paulo / SÃO PAULO` | mesmo rank textual | após o conteúdo próprio; `Equipe: Chapecoense` |
| Coritiba | `/site/items/brasil/teams/coritiba/items/sao-paulo` | mesmos campos | `Item / São Paulo / SÃO PAULO` | mesmo rank textual | após o conteúdo próprio; `Equipe: Coritiba` |
| Ituano | `/site/items/brasil/teams/ituano/items/sao-paulo` | mesmos campos | `Item / São Paulo / SÃO PAULO` | mesmo rank textual | após o conteúdo próprio; `Equipe: Ituano` |

Nenhum desses itens foi alterado, filtrado ou ocultado.

## Regra determinística de ranking

1. Identidade exata normalizada de equipe ou conteúdo editorial.
2. Conteúdo da própria equipe quando existe exatamente uma identidade de equipe inequívoca.
3. Correspondências parciais de identidade de equipe/editorial.
4. Correspondências textuais secundárias da API, preservando sua ordem relativa.

A igualdade aceita acentos, espaços e hífens apenas para comparação. Quando uma consulta sem acento identifica exatamente uma equipe, o display name existente é usado como consulta complementar à mesma API; isso permite que `Sao Paulo` recupere o mesmo conteúdo de `São Paulo` sem criar índice, alterar backend ou inventar resultados. A deduplicação continua baseada em tipo, país, equipe, coleção, item e rota.

## Apresentação

Resultados de item e coleção mantêm seu título persistido. O subtítulo passa a informar `Equipe: {teamDisplayName}` quando a equipe proprietária existe na lista pública. Resultados de equipe preservam o padrão existente. Nenhum CSS ou estrutura visual global foi alterado.

## Resultados validados

- `São Paulo` e `Sao Paulo`: equipe São Paulo; item do próprio São Paulo; depois Caxias, Chapecoense, Coritiba e Ituano, todos identificados pela equipe real.
- `Atlético-MG` e `Atletico-MG`: Atlético-MG em primeiro.
- `Atlético`: Atlético-MG e seu conteúdo diretamente associado precedem identidades parciais e conteúdo secundário, conforme a hierarquia aprovada.
- `América-MG` e `America-MG`: América-MG em primeiro.
- `América`: América-RN, Club América, América-MG e América-RJ permanecem encontráveis antes dos itens textuais.
- `Grêmio` e `Gremio`: Grêmio em primeiro.
- `Juventus`: equipe seguida pelos dois itens da própria Juventus.
- `Chicão` e `Chicao`: memorial editorial `/site/chicao` em primeiro.
- termo genérico `1988`: 91 itens continuaram pesquisáveis.
- `zz-et-026a-inexistente`: zero resultados, sem aproximação artificial.

## Arquivos

Criado:

- `docs/et-026a-search-ranking-report.md`

Alterados:

- `frontend/src/public/utils/publicSearch.ts`
- `frontend/src/public/utils/publicSearch.test.mjs`
- `frontend/src/public/pages/PublicPages.tsx`
- `README.md`
- `docs/changelog.md`
- `docs/roadmap.md`

Removidos: nenhum. CSS alterado: nenhum. Backend/API/banco alterados: nenhum.

## Validação e integridade

- ESLint: aprovado.
- Testes de nomes: 6/6.
- Testes específicos da busca: 10/10.
- Build Vite/TypeScript: aprovado.
- Backend: 112/112 testes aprovados; uma advertência de depreciação do Starlette.
- HTTP 200: `/site`, `/site/equipes`, `/site/chicao`, `/site/busca` e destinos de São Paulo, Atlético-MG, América-MG e Grêmio.
- Antes/depois: 3 países, 175 equipes, 930 coleções, 4.465 itens, 16.417 relações de mídia, 351 coleções vazias e oito itens `ready` sem mídia.

Os avisos transparentes dos oito itens sem mídia foram preservados. Não houve rebuild de Inventory, Parser, Catalog, Normalization, View Model, Media Layer ou Historical Collections. Workspace, assets, slugs, IDs, stable keys, nomes persistidos, resolvers, Team Branding, Home, homenagem, menu, memoriais e vídeos permaneceram intactos. Nenhum commit ou push foi executado.

Validação visual final pendente para aprovação manual do usuário; não havia navegador conectado à sessão.
