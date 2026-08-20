# ET-029D — Isolamento de `fot_gio` e plano de propagação

## 1. Resumo executivo

**Decisão: `OPTION_C_REQUIRES_FULL_DEPENDENT_REBUILD`.** O subconjunto Catalog de 698 itens é seguro isoladamente e mantém `fot_gio` em 11, mas a propagação suportada hoje exige novos runs completos de Normalization e View. A Normalization coerente altera 698 stable keys e, por consequência da regra `SL002`, 698 slugs. O View completo cria somente 172 relações de mídia porque `catalog_item_images` está vazio, contra 16.417 no View oficial, e não possui Media run compatível. Nenhuma aplicação oficial foi executada.

## 2. Baseline

Oficial preservado: Catalog 10, Quality 7, Normalization 9, View 15, Media 17 e Historical Collections 1. Totais: 3 países/regiões, 175 equipes, 930 coleções, 4.465 itens, 351 coleções públicas vazias, 8 itens ready sem mídia, zero `catalog_item_images` e 16.417 mídias no View.

## 3. Os cinco registros `fot_gio`

Todos vêm de `paises/italia/roma/8384.htm`, pertencem à equipe Roma, mas o Catalog 10 aponta para a coleção `camisas/italia/torino/fot_gio`. Cada grupo HTML contém três referências resolvidas para a coleção candidata da própria Roma.

| ID | Stable key atual | Slug público | Identidade | Coleção candidata | Evidência | Mídia View |
|---:|---|---|---|---|---|---:|
| 45778 | `item:da7c899b…f5dc2` | `1983-1984-503430` | `hx001:table-118:description-table-127` | Roma `03_20` | 3 refs; T. Cerezo | 3 |
| 45779 | `item:910a7482…f36f` | `1983-1984-5c36f0` | `hx001:table-143:description-table-152` | Roma `04_21` | 3 refs; C. Ancelotti | 3 |
| 45780 | `item:ff9b659c…fc808` | `1983-1984-17e9b8` | `hx001:table-163:description-table-172` | Roma `09_23` | 3 refs; Chierico | 3 |
| 45781 | `item:0917e0e6…3c611` | `1983-1984-544777` | `hx001:table-183:description-table-192` | Roma `02_25` | 3 refs; F. Graziani | 3 |
| 45783 | `item:83ea7a17…4f9e9` | `1983-1984-bcb7ab` | `hx001:table-228:description-table-237` | Roma `02_25` | 3 refs; S. Nela | 3 |

## 4. Classificação individual

Os cinco são `DATA_MODEL_ANOMALY`: há desacordo entre `catalog_items.team_id=Roma` e `catalog_items.collection_id=Torino/fot_gio`, permitido porque nenhuma FK composta garante que item e coleção pertençam à mesma equipe. Não são cross-team na evidência histórica: página, contexto e imagens apontam para Roma. Foram incluídos nos 703 porque suas referências por registro são exclusivas e determinísticas. Apesar de haver evidência para movê-los, foram excluídos porque a ET proíbe decidir/corrigir `fot_gio` e exige 11→11.

## 5. Subconjunto seguro

`AUTHORIZED_SAFE_SUBSET`: **698** registros `SAFE_TO_MOVE`. `EXCLUDED_FOT_GIO`: **5** registros `DATA_MODEL_ANOMALY`. O número real coincide com a expectativa, sem ser forçado. Nenhum `OTHER`, `MIXED`, ambíguo ou cross-team foi incluído.

## 6. Simulação Catalog

Em cópia temporária: 698/698 `collection_id` atualizados; 4.465 itens antes/depois; IDs, equipes, paths e slugs-base preservados; zero item criado, removido ou duplicado; zero `catalog_item_images`; 536 extras e 217 mistos intactos; `fot_gio` 11→11.

## 7. Coleções recuperadas

- vazias antes: 351;
- vazias depois do Catalog seletivo: 91;
- recuperadas: **260**;
- diferença contra ET-029C: menos 3;
- preenchidas que ficam vazias: **0**.

Roma `03_20`, `04_21` e `09_23` permanecem vazias por conterem somente itens excluídos. Roma `02_25` é parcialmente recuperada por outro item seguro, mas deixa de receber os dois excluídos.

## 8. As 30 coleções da ET-029B

30/30 permanecem preenchidas. Nenhuma fica vazia porque a migração seletiva não aplica as remoções globais que causaram o gate da ET-029B.

## 9. IDs

Todos os 4.465 IDs e os 698 IDs afetados foram preservados. `team_before == team_after` para 698/698.

## 10. Stable keys

698/698 stable keys precisam mudar quando a associação correta é materializada. A fórmula oficial usa `item + parent stable key + relative_path`; portanto, a chave representa identidade lógica/editorial contextualizada no Catalog, não identidade física da mídia. Preservar a chave antiga seria database-valid, mas semanticamente incorreto. Não houve colisão na simulação.

## 11. Slugs

O slug-base do Catalog é preservado. Porém, na Normalization oficial, todos os 698 itens usam resolução `SL002`; como o sufixo é hash da stable key, **698/698 slugs públicos mudam** após o recálculo coerente. Os 536 extras e 217 mistos mantiveram stable key, collection key e slug sem mudança.

## 12. Rotas

698/698 rotas são classificadas como `BOTH`: mudam o segmento de coleção e o slug derivado da nova stable key. Não houve rota duplicada entre 4.465 itens. O mapa integral está em `docs/et-029d-route-impact.csv`. Nenhuma rota antiga do subconjunto foi encontrada hardcoded em `frontend/src` ou `backend/app`; referências aparecem apenas nos relatórios/CSVs técnicos. Uma futura publicação ainda precisa de aliases/redirects por compatibilidade externa.

## 13. Quality

Quality 7 permanece database-valid e ligada ao Catalog 10, mas semanticamente anterior à troca. Não há issues de item para os 703 originais, logo não há review/issue individual a reconciliar neste subconjunto. Uma aplicação real deve executar Quality novamente antes de Normalization.

## 14. Normalization

Normalização atual após somente Catalog: `DATABASE_VALID=YES`, `SEMANTICALLY_VALID=NO`. `source_entity_id` continua válido, mas stable key e collection stable key ficam antigas. O mecanismo existente suporta somente novo run completo; não existe API/repositório incremental. No protótipo, após recalcular as stable keys no Catalog temporário, o run 10 processou 3 países, 175 equipes, 930 coleções e 4.465 itens; exatamente 698 itens mudaram stable key, collection key e slug.

## 15. View

Após somente Catalog: `DATABASE_VALID=YES`, `SEMANTICALLY_VALID=NO`, `PUBLICLY_CORRECT=NO`. Collection slug, rota, breadcrumb e agrupamento vêm da Normalization. O mecanismo existente suporta somente novo View run completo. O run temporário 16 gerou 4.465 itens, 4.465 rotas únicas e zero colisão, mas somente 172 relações de mídia.

## 16. Media Layer

As imagens do Media 17 continuam fisicamente servíveis por suas media keys, mas o View Repository só enriquece mídia através de um Media run cujo `catalog_view_run_id` seja o View consultado. O View temporário 16 não possui tal run. Além disso, como `catalog_item_images=0`, o View oficial reconstruído perde as 16.245 relações de item e conserva essencialmente branding (172). Resultado: 4.464 itens ready sem mídia no View candidato, contra 8 oficiais. Um View novo não pode ser publicado sem recuperar relações e executar Media coordenadamente.

## 17. Chicão

- São Paulo 1977: `/items/brasil/teams/saopaulo/collections/fot-gio/1977-5336f6`, fora do subconjunto, inalterada;
- Seleção Brasileira 1978: `/items/brasil/teams/selecaob/items/1978`, fora do subconjunto, inalterada;
- Atlético-MG 1979: `/items/brasil/teams/atletico/collections/10-12/1979-ae6fca`, item 42421 `OTHER/BLOCKED_AMBIGUOUS`, fora do subconjunto, inalterada.

Excluindo os cinco `fot_gio`, a rota memorial do Atlético-MG não perde coleção nem exige alteração de frontend.

## 18. Os 536 extras

536/536 mantiveram associação Catalog, stable key, collection key e slug durante Catalog seletivo e Normalization simulada. Qualquer futura execução deve repetir esse gate.

## 19. Os 217 mistos

217/217 permaneceram sem nova associação e mantiveram stable key, collection key e slug. Nenhum desempate automático foi realizado.

## 20. MEDIA_ONLY

14/14 permaneceram intactas e vazias no Catalog seletivo.

## 21. LEGITIMATELY_EMPTY

2/2 permaneceram intactas e vazias.

## 22. Oito itens sem mídia

Catalog seletivo e View oficial preservado: 8→8. O View temporário reconstruído falha esse gate: 4.464 itens ready sem mídia, devido à ausência histórica de `catalog_item_images`.

## 23. FKs

Após Catalog, Normalization e View temporários: `PRAGMA foreign_key_check` retornou zero erros. A falta de coerência de mídia é lógica, não uma violação de FK.

## 24. Integridade

`PRAGMA integrity_check=ok`; zero stable keys duplicadas; zero rotas duplicadas; 4.465 itens; equipes e IDs preservados. As cópias temporárias foram descartadas.

## 25. Script

O script ET-029C foi evoluído apenas para receber `--expected-count`, permitindo exigir exatamente 698 linhas. Dry-run, transação, rollback, baseline, whitelist, mesma equipe, proteção `fot_gio`, idempotência, integridade, FKs e recusa do banco oficial permanecem. Propagação Normalization/View não foi incorporada porque a arquitetura só oferece runs completos e o View resultante falha o gate de mídia; implementar updates manuais in-place violaria a imutabilidade dos runs.

## 26. Testes

O teste específico de cardinalidade segura foi adicionado. A suíte do script passou em **10/10** e cobre dry-run/rollback, apply, idempotência, identidade, divergências, alvo ausente/cross-team, proteção `fot_gio`, whitelist e recusa da base oficial. Stable-key/route collision e propagação foram validados no protótipo real, não adicionados como caminho executável porque a estratégia foi reprovada. Backend completo: **132/132 PASS**. Frontend: nomes **6/6**, busca **11/11**, lint e build PASS.

## 27. Riscos

- 698 URLs mudariam simultaneamente por coleção e slug;
- inexistência de redirects/aliases gerais;
- novo View sem relações históricas de item;
- Media 17 não é compatível com um novo View run;
- atualização incremental in-place não é mecanismo oficial e quebraria auditabilidade;
- os cinco itens Roma/Torino continuam como anomalia deliberadamente preservada.

## 28. Estratégia escolhida

`OPTION_C_REQUIRES_FULL_DEPENDENT_REBUILD`. A menor estratégia suportada é: Catalog seletivo + recálculo de stable keys + novo Quality + novo Normalization completo + novo View completo + recuperação controlada de `catalog_item_images`/relações históricas + novo Media run + aliases das rotas antigas. Como Media e `catalog_item_images` estão proibidos nesta ET, não existe sequência publicável Catalog/Normalization/View isolada.

## 29. Critérios para ET-029E

Uma futura autorização deve incluir explicitamente: snapshot/rollback; whitelist 698; política para os cinco `fot_gio`; recomposição auditável de relações de mídia sem itens novos; Quality; Normalization/View completos ou um mecanismo incremental oficialmente implementado; Media compatível; mapa de 698 redirects; gates Chicão, busca, 536 extras, 217 mistos, 14 MEDIA_ONLY, 2 LEGITIMATELY_EMPTY e 8 itens sem mídia. ET-029E não foi iniciada.

## 30. Integridade oficial preservada

Nenhum Catalog, Quality, Normalization, View, Media ou Historical Collections oficial foi criado, alterado ou reconstruído. Banco oficial: 445.566.976 bytes, `mtime_ns=1787141730427370700`, `integrity_check=ok`, zero FKs, runs 10/9/15/17 e 4.465 itens. Nenhum frontend, busca, asset, HTML histórico ou banco oficial foi alterado. As 6 páginas públicas, 6 buscas protegidas e 3 rotas memoriais responderam HTTP 200. Nenhum commit ou push foi realizado.
