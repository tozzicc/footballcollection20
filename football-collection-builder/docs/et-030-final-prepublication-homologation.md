# ET-030 — Homologação final pré-publicação

## 1. Resumo executivo

**Resultado técnico:** não foi encontrada regressão nova. O banco, as camadas públicas, as 7.137 rotas visuais atuais, os 260 destinos recuperados, as 698 rotas novas, a busca, o memorial do Chicão, as mídias e os testes passaram. Resta exclusivamente a homologação visual manual.

## 2. Decisão

`OPTION_A_READY_FOR_VISUAL_HOMOLOGATION`.

## 3. Baseline pós-029G

3 países/regiões, 175 equipes, 930 coleções, 4.465 itens em Catalog/Normalization/View, 4.457 com mídia, 8 sem mídia, 91 coleções vazias, 16.245/16.417/16.618 relações e 15.592 assets disponíveis.

## 4. Integridade

`PRAGMA integrity_check=ok`; `PRAGMA foreign_key_check=0`; zero colisão de rota e zero colisão de stable key.

## 5. Runs

Catalog 10, Normalization 10, View 16, Media 18 e Historical Collections 1. Nenhum run foi criado.

## 6. Países

PASS/WARNING/FAIL = **3/0/0**. Brasil, Itália e Outros têm slug, display, API, rota e navegação válidos.

## 7. Equipes

PASS/WARNING/FAIL = **169/6/0**. As 175 APIs e rotas visuais responderam 200; nomes editoriais e país estão coerentes. As seis equipes sem logo usam fallback conhecido: Internacional de Limeira, Alzano Virescit, Cerro (Uruguai), Sporting CP, Universidad de Chile e Vitória de Setúbal.

## 8. Coleções

PASS/WARNING/FAIL = **839/91/0**. As 930 APIs e rotas responderam 200; 839 possuem itens e 91 são vazias conhecidas.

## 9. 260 recuperadas

PASS/WARNING/FAIL = **260/0/0**. Todas constavam vazias no artefato ET-029G, agora possuem itens, pertencem à equipe esperada e têm API/rota acessível.

## 10. 91 vazias

Confirmadas e classificadas como `KNOWN_DEBT`: 14 `MEDIA_ONLY`, 2 `LEGITIMATELY_EMPTY` e 75 remanescentes das auditorias anteriores. Nenhuma das 260 recuperadas voltou a ficar vazia.

## 11. 698 rotas novas

PASS/WARNING/FAIL = **698/0/0**. Team, collection, slug e item correspondem ao mapping aprovado; todas estão no View 16, responderam 200 e não possuem colisão.

## 12. Rotas antigas

`OLD_ROUTE_NOT_FOUND=698`, `OLD_ROUTE_STILL_VALID=0`, `OLD_ROUTE_REDIRECT=0`, `OLD_ROUTE_POINTS_ELSEWHERE=0`. Os 698 endpoints semânticos antigos respondem 404. Como o site ainda não foi publicado, trata-se de impacto de migração conhecido, não bloqueador.

## 13. Itens

Total 4.465. PASS/WARNING/FAIL = **4.457/8/0**. Todos os endpoints semânticos e rotas visuais responderam 200.

## 14. 8 sem mídia

Os mesmos oito IDs aprovados permanecem sem relação Catalog: `KNOWN_MISSING_MEDIA=8`; `NEW_MISSING_MEDIA=0`.

## 15. Media Layer

Catalog 16.245; View 16.417; Media 16.618; assets disponíveis 15.592; zero indisponível, inválido, vazio, path ausente ou MIME incompatível.

## 16. Imagens

PASS/WARNING/FAIL = **15.610/0/0**: 15.592 imagens da Media Layer e 18 imagens/assets estáticos públicos. Todos os assets Media responderam 200/206; dimensões e tamanhos são válidos.

## 17. Vídeos

PASS/WARNING/FAIL = **3/0/0**. Os três MP4 do Chicão têm tamanho positivo, `video/mp4`, suporte Range e resposta 206.

## 18. Home

Estrutura fonte e rota aprovadas: hero oficial, países, equipes em destaque e homenagem imediatamente após os destaques. O PNG `chicao-memorial-home.png` permanece utilizado.

## 19. Menu

Início, Países, Equipes, Coleções, Homenagem e Últimas inclusões preservados. Homenagem aponta para `/site/chicao`.

## 20. Chicão

PASS estrutural e HTTP: breadcrumb, título, imagem documental, depoimento de Mauro Matta, quatro cards, memória audiovisual e três vídeos permanecem presentes.

## 21. Busca

PASS para 14 consultas obrigatórias. Consultas exatas retornam somente a equipe correta; Chicão retorna somente o editorial; América retorna busca ampla legítima; 1988 retorna resultados globais; termo inexistente retorna zero.

## 22. Links internos

PASS/REDIRECT/WARNING/FAIL = **7.137/0/0/0** no universo visual deduplicado atual. APIs semânticas correspondentes também foram exercitadas integralmente.

## 23. Breadcrumbs

4.465/4.465 JSON válidos, com sequência country/team/[collection]/item, labels e slugs presentes. Rotas de país, equipe, coleção, temporada e Chicão foram validadas estruturalmente.

## 24. Metadados

Zero ocorrência de título/nome vazio, `undefined`, `null`, `[object Object]` ou `NaN` em países, equipes, coleções e itens. Os 175 display names foram resolvidos; os seis ambíguos continuam preservados.

## 25. Cross-team

24 conhecidas; NEW=0; WORSENED=0; 24/24 identidades iguais ao baseline ET-029F. As 13 HIGH editoriais continuam `KNOWN_DEBT`, não HIGH novo.

## 26. fot_gio

11 itens preservados. A anomalia histórica não foi corrigida nem agravada.

## 27. 536 extras

536/536 inalterados contra o snapshot pré-029G.

## 28. 217 mistos

217/217 inalterados contra o snapshot pré-029G.

## 29. MEDIA_ONLY

14/14 vazias, conforme baseline aceito.

## 30. LEGITIMATELY_EMPTY

2/2 vazias, conforme baseline aceito.

## 31. HTTP

30.024 alvos únicos auditados. Após percent-encoding correto das 785 temporadas com en dash, todos os alvos atuais responderam 200/206. O universo inclui APIs e rotas de 3 países, 175 equipes, 930 coleções, 1.500 temporadas, 4.465 itens, 196 itens históricos, 15.592 mídias, páginas principais e assets estáticos.

## 32. 404

404 relevante atual: **0**. As 698 rotas antigas retornam 404 semântico esperado e ficam fora da contagem de falha atual.

## 33. 5xx

HTTP 500/502/503: **0**. Nenhuma exception, traceback ou falha interna foi observada no crawler ou nos testes.

## 34. Frontend

Nomes team/country 6/6 PASS; busca 11/11 PASS; auditoria integrada das 14 consultas obrigatórias PASS.

## 35. Backend

Pytest completo: **134/134 PASS**, com apenas o warning de depreciação conhecido do TestClient/Starlette.

## 36. Responsividade

`VISUAL_REVIEW_REQUIRED`. Não havia navegador conectado para 1440, 768 e 390 px; nenhuma aprovação visual foi inventada.

## 37. Console

Não inspecionado por indisponibilidade de navegador conectado. Limitação classificada como `VISUAL_REVIEW`, não regressão.

## 38. Comparação ET-025

O universo visual deduplicado permaneceu em 7.137. ET-025: PASS 6.758, WARNING 371, FAIL 8. ET-030: **PASS 7.019, WARNING 118, FAIL 0**. As 261 coleções vazias recuperadas migraram de warning para pass; os oito itens sem mídia permanecem, mas agora são baseline conhecido em warning; 91 vazias, 6 fallbacks e 13 cross-team HIGH conhecidas explicam os 118 warnings atuais.

## 39. NEW_REGRESSION

Nenhuma: **0**.

## 40. KNOWN_DEBT

91 coleções vazias; 24 cross-team, sendo 13 HIGH editoriais; 8 itens sem mídia; 14 `MEDIA_ONLY`; 2 `LEGITIMATELY_EMPTY`; 536 extras; 217 mistos; seis fallbacks de logo; ambiguidades históricas documentadas; 698 rotas antigas sem redirect antes da primeira publicação.

## 41. VISUAL_REVIEW

Revisão manual necessária para desktop 1440 px, tablet 768 px e mobile 390 px nas páginas Home, Equipes, São Paulo, coleção, item, Busca e Chicão, incluindo console, overflow, menu, cards, imagens, vídeos, breadcrumbs e links.

## 42. CRITICAL

`CRITICAL_NEW=0`.

## 43. HIGH

`HIGH_NEW=0`. Os 13 HIGH preexistentes permanecem dívida conhecida.

## 44. MEDIUM

`MEDIUM_NEW=0`.

## 45. LOW

`LOW_NEW=0`.

## 46. Gate de publicação

`OPTION_A_READY_FOR_VISUAL_HOMOLOGATION`: todos os gates técnicos obrigatórios passaram e resta somente validação visual/manual.

## 47. Próximo passo

Executar a **validação visual manual do usuário**. Não iniciar ET-030A, ET-031 ou publicação automaticamente.

## 48. Integridade do banco

Ao final: 3/175/930/4.465, runs 10/10/16/18/1, `integrity_check=ok` e FK=0. Nenhuma mutação ou rebuild ocorreu durante a ET-030.

## 49. Arquivos criados

Somente `docs/et-030-final-prepublication-homologation.md`. Nenhum CSV de falha foi necessário porque não houve exceção atual.

## 50. Confirmação read-only

Banco, frontend, backend, assets, README, changelog e roadmap permaneceram intactos. Nenhum run, correção, commit ou push foi realizado.
