# ET-026B — Busca contextual por entidade

## Resultado

Consultas que resolvem exatamente e de forma inequívoca uma equipe agora entram no contexto estrutural dessa equipe. O resultado contém a entidade e somente conteúdo cujo `countrySlug` e `teamSlug` comprovem pertencimento. Correspondências textuais de outras equipes deixam de participar desse contexto, sem alteração ou exclusão dos registros históricos.

Quando não há uma equipe exata única, a busca global da ET-026/026A continua funcionando. O memorial Chicão permanece como entidade editorial própria.

## Arquitetura encontrada

O fluxo público permanece:

`query → normalizePublicSearchTerm → equipes públicas/teamDisplayName → aliases da API → merge/deduplicação → ranking → apresentação`

Normalização, resolução, aliases, ranking e transformação já estavam centralizados em `frontend/src/public/utils/publicSearch.ts`. O componente React apenas busca os dados e renderiza o resultado. Nenhuma regra foi duplicada no JSX.

## Causa raiz e comportamento anterior

A ET-026A identificava corretamente uma equipe exata e promovia seu conteúdo, mas depois mantinha as correspondências textuais globais. Assim, Caxias, Chapecoense, Coritiba e Ituano continuavam na consulta “São Paulo” porque seus itens têm `title = São Paulo` e `original_title = SÃO PAULO`, embora seus vínculos estruturais apontem para outras equipes.

## Solução

Após deduplicar os resultados:

- se houver exatamente uma equipe resolvida, permanecem somente resultados com o mesmo `countrySlug/teamSlug`;
- se a consulta for exatamente `Chicão`/`Chicao`, permanece somente o resultado editorial `/site/chicao`;
- sem identidade exata inequívoca, nenhum filtro contextual é aplicado e a pesquisa textual global permanece intacta.

A igualdade reutiliza a normalização da ET-026A e aceita acentos, espaços e hífens apenas para comparação. Pertencimento nunca é inferido por título, descrição ou outro texto.

## Ordem real — São Paulo

Para `São Paulo` e `Sao Paulo`, a ordem real é:

1. `Equipe — São Paulo` → `/site/paises/brasil/equipes/saopaulo`
2. `Item — São Paulo — Equipe: São Paulo` → `/site/items/brasil/teams/saopaulo/items/sao-paulo`

Total: 2 resultados. Não aparecem Caxias, Chapecoense, Coritiba, Ituano ou qualquer equipe sem vínculo estrutural com `brasil/saopaulo`.

## Consultas validadas

- `São Paulo` / `Sao Paulo`: dois resultados contextuais, ambos de `brasil/saopaulo`.
- `Atlético-MG` / `Atletico-MG`: contexto exclusivo de `brasil/atletico`.
- `América-MG` / `America-MG`: contexto exclusivo de `brasil/america-mg`.
- `América`: continua global; quatro identidades legítimas e dois itens foram retornados.
- `Grêmio` / `Gremio`: contexto exclusivo de `brasil/gremio`.
- `Chicão` / `Chicao`: somente o memorial `/site/chicao`.
- `1988`: busca global preservada, com 91 resultados de diversas equipes.
- `zz-et-026b-inexistente`: zero resultados.

## Arquivos

Criado:

- `docs/et-026b-contextual-search-report.md`

Alterados:

- `frontend/src/public/utils/publicSearch.ts`
- `frontend/src/public/utils/publicSearch.test.mjs`
- `README.md`
- `docs/changelog.md`
- `docs/roadmap.md`

Removidos: nenhum. `PublicPages.tsx`, CSS, backend, API e banco não precisaram ser alterados nesta ET.

## Testes e HTTP

- ESLint: aprovado.
- Testes existentes de nomes: 6/6.
- Testes da busca, incluindo os casos ET-026B: 11/11.
- Build TypeScript/Vite: aprovado.
- Backend: 112/112 testes; uma advertência de depreciação do Starlette.
- HTTP 200: `/site`, `/site/paises`, `/site/equipes`, `/site/colecoes`, `/site/ultimas`, `/site/chicao`, `/site/busca` e destinos contextuais verificados.

## Integridade

Antes/depois: 3 países, 175 equipes, 930 coleções, 4.465 itens, 16.417 relações de mídia, 351 coleções vazias e oito itens `ready` sem mídia.

Banco, workspace histórico, assets, imagens, vídeos, Inventory, Parser, Catalog, Normalization, View Model, Media Layer, Historical Collections, rotas, slugs, IDs, stable keys, Team Branding, Home, menu e memorial permaneceram intactos. Os avisos transparentes dos oito itens sem mídia foram preservados. Nenhuma camada foi reconstruída. Nenhum commit ou push foi executado.

Os serviços locais permanecem ativos. Validação visual final pendente para aprovação manual do usuário, pois não há navegador conectado à sessão.
