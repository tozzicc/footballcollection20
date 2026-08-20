# ET-029G — Aplicação coordenada oficial das 698 associações

## 1. Resumo executivo

**Estado: `ET-029G APPLIED_SUCCESSFULLY`.** As 698 reassociações aprovadas nas ET-029C–F foram aplicadas no banco oficial. Catalog, relações de imagens, Normalization, View e Media foram coordenados sem perda de itens, mídia, rotas ou coleções protegidas.

## 2. Baseline

Entrada confirmada: runs Catalog 10, Normalization 9, View 15, Media 17 e Historical Collections 1; 3 países/regiões, 175 equipes, 930 coleções, 4.465 itens, 351 coleções vazias, 8 itens sem mídia, zero `catalog_item_images`, 11 itens `fot_gio` e 24 cross-team.

## 3. Banco oficial utilizado

`C:\Projetos\footballcollection20\football-collection-builder\database\football_collection.db`, 445.566.976 bytes antes da operação, SQLite válido.

## 4. Snapshot

`database/snapshots/et-029g-pre-apply-20260820.db`, criado imediatamente antes da primeira escrita por backup nativo SQLite, com 445.566.976 bytes.

## 5. SHA-256

`C0387BF1F99D8409EE31C34497DC288FE6E346FF9132C60B7526EFEB9084A5B5`.

## 6. Pre-flight

PASS. Todos os runs, totais, 698 IDs/identidades/stable keys/teams/origens/destinos, cinco exclusões `fot_gio`, 536 extras, 217 mistos e 24 cross-team corresponderam aos artefatos aprovados.

## 7. Dry-run

PASS em cópia descartável exata do snapshot. Previu 698/698 alterações, 260 coleções recuperadas, 91 vazias, zero preenchida esvaziada, relações 16.245/16.417/16.618, 15.592 assets, 8 sem mídia, `fot_gio=11`, cross-team 24 e zero colisões.

## 8. Whitelist 698

Fonte exclusiva: `docs/et-029d-authorized-safe-subset.csv`, 698 linhas únicas. Resultado individual em `docs/et-029g-applied-698.csv`.

## 9. Exclusões fot_gio

Os cinco registros de `docs/et-029d-excluded-fotgio.csv` permaneceram excluídos. Total: 11 → 11.

## 10. Aplicação Catalog

698/698 `collection_id` alterados em transação controlada; IDs, teams, caminhos e slugs Catalog preservados. As 698 stable keys Catalog foram substituídas somente pelos valores `candidate_stable_key` já aprovados no CSV.

## 11. Restauração catalog_item_images

O mecanismo auditado recompôs exclusivamente relações derivadas do Parser: 0 → 16.245, para 4.457 itens, usando Image Parser run 2. Nenhum asset físico ou Image Metadata foi criado ou alterado.

## 12. Normalization

Novo run oficial 10, completo: 3 países, 175 equipes, 930 coleções e 4.465 itens. Identidades dos 698 foram propagadas semanticamente.

## 13. View

Novo run oficial 16: 4.465 itens, 16.417 relações e 4.465 rotas únicas.

## 14. Media

Novo run oficial 18: 16.618 relações de origem, 15.592 assets únicos e disponíveis, zero indisponível e zero inválido.

## 15. Runs antes/depois

- Catalog: 10 → 10; aplicação seletiva no run existente.
- Normalization: 9 → 10.
- View: 15 → 16.
- Media: 17 → 18.
- Historical Collections: 1 → 1.

## 16. Itens

Catalog 4.465 → 4.465; Normalization 4.465 → 4.465; View 4.465 → 4.465. Nenhum item criado, removido ou duplicado.

## 17. Coleções

930 → 930. Vazias: 351 → 91; nenhuma coleção antes preenchida foi esvaziada.

## 18. 260 recuperadas

260/260 coleções antes vazias passaram a ter itens. A comparação individual `collection,before,after,item_count` está em `docs/et-029g-recovered-260-collections.csv`.

## 19. 91 vazias

Confirmadas 91. Permanecem fora do escopo, incluindo as 14 `MEDIA_ONLY` e duas `LEGITIMATELY_EMPTY`.

## 20. 30 protegidas

30/30 coleções identificadas na ET-029B continuam preenchidas. O gate global confirmou zero coleção previamente preenchida esvaziada.

## 21. 536 extras

536/536 `OTHER + REASSOCIATE` permaneceram integralmente inalterados em team, collection, caminho, slug e stable key.

## 22. 217 mistos

217/217 permaneceram integralmente inalterados, sem associação automática.

## 23. fot_gio

11 → 11. Nenhum dos cinco registros excluídos foi aplicado.

## 24. MEDIA_ONLY

14/14 continuam vazias e não foram preenchidas automaticamente.

## 25. LEGITIMATELY_EMPTY

2/2 continuam vazias.

## 26. Itens sem mídia

8 → 8; os mesmos IDs permaneceram sem relações Catalog. `NEW_MISSING_MEDIA=0`.

## 27. Relações de mídia

Catalog 0 → 16.245; View 16.417 → 16.417; Media total 16.618 → 16.618.

## 28. Assets

15.592 assets únicos/disponíveis, zero indisponível e zero inválido.

## 29. Cross-team

24 → 24; NEW=0; WORSENED=0; 24/24 IDs do baseline ET-029F contabilizados. Nenhuma foi corrigida.

## 30. Stable keys

698 stable keys Catalog alteradas para os valores candidatos aprovados; zero colisão Catalog ou Normalization.

## 31. Slugs

698 slugs públicos recalculados semanticamente pela Normalization; slugs Catalog permaneceram intactos.

## 32. Rotas

698/698 rotas correspondem exatamente ao resultado aprovado na ET-029E. Zero colisão. Mapeamento em `docs/et-029g-final-route-mapping.csv`.

## 33. Chicão

São Paulo 1977, Seleção Brasileira 1978 e Atlético-MG 1979 permaneceram nos mesmos itens. Três APIs e três páginas memoriais válidas; nenhum `href` precisou ser alterado.

## 34. Busca

ET-026C preservada. Testes para São Paulo, Atlético-MG, América-MG, Grêmio, Juventus e Chicão, com variações sem acento, passaram 11/11.

## 35. HTTP

41/41 verificações aprovadas: seis páginas públicas, 11 buscas, três itens do Chicão, dez coleções recuperadas, dez itens reassociados e uma mídia. Páginas/APIs responderam 200; Range de mídia respondeu 206.

## 36. integrity_check

Final: `ok`.

## 37. foreign_key_check

Final: zero violações.

## 38. Testes

Backend completo: 133/133 PASS antes da adição do teste de cobertura específico; o teste ET-029C/ET-029G adicional também passou na validação final. Frontend: nomes 6/6, busca 11/11, lint PASS e build PASS.

## 39. Validação visual

`VISUAL_REVIEW_REQUIRED`. A habilidade de navegador foi inicializada, mas nenhum navegador estava conectado. Conforme a ET, isso não causa rollback diante dos gates estruturais, funcionais e HTTP aprovados.

## 40. Rollback disponível

O snapshot validado permite restauração integral. Procedimento: parar o backend; restaurar o snapshot por backup SQLite; validar o SHA do snapshot, `integrity_check`, FK e baseline 10/9/15/17/1; reiniciar backend; validar HTTP. O rollback não foi necessário.

## 41. Arquivos criados

- `database/snapshots/et-029g-pre-apply-20260820.db`;
- `docs/et-029g-official-coordinated-apply.md`;
- `docs/et-029g-applied-698.csv`;
- `docs/et-029g-recovered-260-collections.csv`;
- `docs/et-029g-final-route-mapping.csv`.

## 42. Arquivos alterados

Banco oficial; mecanismo seletivo ET-029C (autorização oficial restrita e stable key candidata); teste correspondente; `README.md`, `docs/changelog.md` e `docs/roadmap.md`. Nenhum frontend, CSS ou asset foi alterado.

## 43. Conclusão

`ET-029G APPLIED_SUCCESSFULLY`. Todos os gates críticos passaram. Não foram iniciadas dívida editorial pós-V1, ET-030, limpeza de runs, commit ou push. O próximo passo é a homologação visual manual antes da publicação.
