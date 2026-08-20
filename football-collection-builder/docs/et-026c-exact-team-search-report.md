# ET-026C — Busca exata por equipe

## Alteração sobre a ET-026B

A fronteira contextual foi simplificada no utilitário existente. Quando a consulta resolve uma única identidade exata, o resultado contém somente essa entidade de equipe. Itens, coleções e demais conteúdos — inclusive os pertencentes à própria equipe — não entram no resultado.

Quando não existe identidade exata, mas o termo corresponde a nomes de várias equipes por termo completo, somente essas entidades são retornadas. Sem identidade de equipe ou editorial conhecida, a pesquisa global da API permanece intacta.

Não houve filtro visual: os resultados são removidos da composição lógica antes da renderização.

## Regra final

- equipe exata única → somente a equipe exata;
- múltiplas equipes legitimamente compatíveis → somente as equipes;
- editorial exato Chicão → somente `/site/chicao`;
- nenhuma identidade → busca textual global existente.

A resolução reutiliza `normalizePublicSearchTerm`, `teamDisplayName` e os aliases da ET-026A. Correspondências parciais de equipe exigem termo normalizado completo: `América` corresponde a “América-MG”, enquanto `Brasil` não captura “Seleção Brasileira” por ser apenas prefixo de “Brasileira”.

## Resultados reais

| Consulta | Resultado |
|---|---|
| `São Paulo` | 1 — Equipe São Paulo (`brasil/saopaulo`) |
| `Sao Paulo` | 1 — mesma equipe |
| `Atlético-MG` | 1 — Equipe Atlético-MG |
| `Atletico-MG` | 1 — mesma equipe |
| `América-MG` | 1 — Equipe América-MG |
| `America-MG` | 1 — mesma equipe |
| `América` | 4 equipes — América-RN, Club América, América-MG e América-RJ; zero itens |
| `Grêmio` | 1 — Equipe Grêmio |
| `Gremio` | 1 — mesma equipe |
| `Juventus` | 1 — Equipe Juventus |
| `Chicão` / `Chicao` | 1 — editorial `/site/chicao` |
| `1988` | busca global, 91 itens |
| `Brasil` | busca global, país Brasil e item Seleção Brasileira |
| `zz-et-026c-inexistente` | zero resultados |

O critério principal foi comprovado: `São Paulo` e `Sao Paulo` retornam somente `Equipe / São Paulo / saopaulo`; nenhum item aparece abaixo.

## Arquivos

Criado:

- `docs/et-026c-exact-team-search-report.md`

Alterados:

- `frontend/src/public/utils/publicSearch.ts`
- `frontend/src/public/utils/publicSearch.test.mjs`
- `README.md`
- `docs/changelog.md`
- `docs/roadmap.md`

Removidos: nenhum. Interface, JSX, CSS, backend, API e banco não foram alterados.

## Validação

- ESLint: aprovado.
- Testes de nomes: 6/6.
- Testes da busca: 11/11.
- Build TypeScript/Vite: aprovado.
- Backend: 112/112 testes; uma advertência de depreciação do Starlette.
- HTTP 200: `/site`, `/site/equipes`, `/site/paises`, `/site/colecoes`, `/site/ultimas`, `/site/chicao`, `/site/busca` e rotas das equipes São Paulo, Atlético-MG, América-MG, Grêmio e Juventus.

## Integridade

Antes/depois: 3 países, 175 equipes, 930 coleções, 351 coleções vazias, 4.465 itens, 16.417 relações de mídia e oito itens `ready` sem mídia.

ET-022R, ET-023, ET-023A, ET-024*, ET-025 e ET-026/A/B foram preservadas nos aspectos não substituídos explicitamente pela nova semântica. Home, memorial, menu, vídeos, assets, resolvers, rotas, slugs, IDs, stable keys, banco e workspace permaneceram intactos. Nenhuma camada derivada foi reconstruída; ET-027 não foi iniciada. Nenhum commit ou push foi executado.

Os serviços locais permanecem ativos para validação manual.
