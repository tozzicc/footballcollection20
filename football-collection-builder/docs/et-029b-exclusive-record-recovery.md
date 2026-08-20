# ET-029B — Recuperação controlada dos registros exclusivos

## 1. Resumo executivo

**Estado: BLOCKED_BEFORE_APPLY.** O pre-flight foi concluído em snapshot isolado, mas quatro gates críticos falharam: `fot-gio` mudaria de 11 para 4 itens; o Catalog oficial inevitavelmente repopularia 16.245 linhas em `catalog_item_images`; a regra global reassociaria 1.239 registros, 536 além dos 703 autorizados; e 30 coleções atualmente preenchidas ficariam vazias sem comprovação histórica suficiente. Nenhuma persistência ocorreu no banco oficial.

## 2. Baseline

| Métrica | Inicial | Final oficial |
|---|---:|---:|
| Países/regiões | 3 | 3 |
| Equipes | 175 | 175 |
| Coleções | 930 | 930 |
| Itens | 4.465 | 4.465 |
| Coleções públicas vazias | 351 | 351 |
| Itens ready sem mídia | 8 | 8 |
| `catalog_item_images` | 0 | 0 |
| Mídias View | 16.417 | 16.417 |

Runs preservados: HTML 3, Image 2, Catalog 10, Normalization 9, View 15 e Media 17.

## 3. Snapshot

- Arquivo: `database/snapshots/et-029b-preflight-20260820.db`.
- Formato: cópia SQLite nativa produzida pela API `backup` do SQLite, com origem aberta em `mode=ro`.
- Tamanho: 445.566.976 bytes.
- SHA-256: `C0387BF1F99D8409EE31C34497DC288FE6E346FF9132C60B7526EFEB9084A5B5`.
- Validação: `PRAGMA integrity_check = ok`, 53 tabelas e métricas equivalentes ao baseline.

## 4. Procedimento de rollback

Como nada foi aplicado, rollback não foi necessário. Se fosse necessário: parar os serviços que escrevem no SQLite; validar novamente checksum e `integrity_check` do snapshot; restaurar por backup SQLite/replace atômico do arquivo oficial; reabrir em modo read-only; conferir runs e todas as métricas do baseline antes de reiniciar os serviços. Não foi realizado teste destrutivo no banco oficial.

## 5. Dry-run integral

Uma segunda cópia isolada do snapshot recebeu o pipeline oficial do Catalog com `replace_previous=False`. Resultado candidato:

- 3 países;
- 175 equipes;
- 930 coleções;
- 4.465 itens;
- 16.245 relações de imagem;
- 1.781 issues;
- 2.842 itens associados a coleção;
- 1.623 preservados sem coleção;
- 812 coleções preenchidas;
- 118 coleções vazias.

A tentativa prévia de `replace_previous=True`, ainda somente na cópia, falhou e fez rollback transacional por `FOREIGN KEY constraint failed`: Quality/Normalization/View referenciam o Catalog anterior. Logo, a arquitetura não permite substituir somente o Catalog preservando as camadas posteriores, como exigido nesta ET.

## 6. Contagem de itens

Atual: 4.465. Candidato: 4.465. Nenhum item foi criado, excluído ou clonado. Este gate passou.

## 7. Análise dos 703 exclusivos

Os 703/703 registros ET-028 classificados como exclusivos produziram candidato único, pertencente à mesma equipe e determinístico. Entretanto, o builder corrigido encontrou 1.239 reassociações determinísticas no conjunto global. As 536 adicionais não pertencem ao universo autorizado pela classificação ET-028 e o mecanismo oficial não oferece aplicação seletiva sem edição manual proibida. Gate de escopo: FAIL.

## 8. Proteção dos 217 mistos

217/217 permaneceram sem associação automática. Não houve escolha da primeira coleção, fuzzy matching ou melhor candidato. Gate: PASS.

## 9. Coleções recuperadas

No candidato, 263 coleções atualmente vazias receberiam pelo menos um registro. Distribuição: Brasil 136, Itália 123 e Outros 4. Maiores concentrações: Torino 30, Atlético-MG 29, Juventus 20, Corinthians 19, Santos 19, Grêmio 15 e Palmeiras 14.

## 10. Coleções que permanecem vazias

O candidato possui 118 coleções vazias. As 14 `MEDIA_ONLY` e as 2 `LEGITIMATELY_EMPTY` permanecem vazias. O total diverge do mínimo estimado porque a regra conservadora também remove associações ambíguas de coleções hoje preenchidas.

## 11. Collections becoming empty

30 coleções atualmente preenchidas passariam a zero:

| País | Equipe | Coleção | Itens antes → candidato |
|---|---|---|---:|
| Brasil | América-RJ | `09_23` | 2 → 0 |
| Brasil | Bahia | `04_21` | 1 → 0 |
| Brasil | Bahia | `07_17` | 1 → 0 |
| Brasil | Bahia | `09_18` | 1 → 0 |
| Brasil | Bahia | `10_19` | 1 → 0 |
| Brasil | Chapecoense | `11_17` | 1 → 0 |
| Brasil | Corinthians | `03_25` | 1 → 0 |
| Brasil | Internacional | `12_17` | 1 → 0 |
| Brasil | Palmeiras | `08_14_2` | 1 → 0 |
| Brasil | Palmeiras | `10_09` | 1 → 0 |
| Itália | Bologna | `09_15` | 1 → 0 |
| Itália | Cagliari | `03_14` | 2 → 0 |
| Itália | Cagliari | `04_20` | 1 → 0 |
| Itália | Cagliari | `08_18_3` | 1 → 0 |
| Itália | Fiorentina | `06_18` | 1 → 0 |
| Itália | Internazionale | `03_20` | 2 → 0 |
| Itália | Itália | `02_13` | 1 → 0 |
| Itália | Itália | `08_14` | 1 → 0 |
| Itália | Itália | `10_13` | 1 → 0 |
| Itália | Juventus | `20-30` | 5 → 0 |
| Itália | Juventus | `60-70` | 7 → 0 |
| Itália | Lazio | `04_20` | 1 → 0 |
| Itália | Milan | `02_15` | 1 → 0 |
| Itália | Milan | `11_17` | 1 → 0 |
| Itália | Napoli | `03_19` | 1 → 0 |
| Itália | Sampdoria | `06_13` | 1 → 0 |
| Itália | Torino | `filadelfia` | 1 → 0 |
| Itália | Torino | `grandetorino` | 1 → 0 |
| Itália | Torino | `outros` | 2 → 0 |
| Outros | Boca Juniors | `01_26` | 1 → 0 |

Não há evidência suficiente nesta ET para declarar todos esses esvaziamentos historicamente corretos. Gate: FAIL.

## 12. Distribuição por equipe

Os totais de itens por equipe são idênticos entre Catalog atual e candidato; nenhuma identidade de equipe mudou. O CSV auxiliar contém o diff item a item. A distribuição de coleções preenchidas muda por reassociação e bloqueio conservador.

## 13. Stable keys

2.043 item stable keys mudariam porque o parent collection stable key participa do hash; 2.422 permaneceriam iguais. A chave é usada pela Normalization e por reconciliação interna, mas não é exposta diretamente nas rotas públicas. A mudança é coerente com a identidade correta, porém exige propagação conjunta e auditoria de reviews. Gate de impacto: conhecido, mas não aprovado para aplicação isolada.

## 14. IDs

Os 4.465 IDs candidatos diferem dos IDs atuais porque o run adicional usa novos autoincrements. IDs são internos e não aparecem nas rotas públicas, mas são FKs das camadas derivadas. Isso explica a falha ao substituir o Catalog sem reconstruir dependentes.

## 15. Slugs

No nível Catalog, 0/4.465 slugs-base mudaram. A Normalization não foi reconstruída; portanto, efeitos finais de `SL002` após mudança de escopo não foram materializados. Esse impacto incompleto impede afirmar segurança total dos slugs públicos.

## 16. Rotas antes/depois

2.043 rotas provisórias mudariam por troca/remoção do segmento de coleção; não foram encontradas colisões usando os slugs públicos atuais. Como a Normalization candidata não foi executada, o resultado é preflight, não rota publicável definitiva. O mapa integral está em `docs/et-029b-item-route-mapping.csv`.

## 17. Links do Chicão

- São Paulo 1977 (`fot-gio/1977-5336f6`): associação permanece igual no Catalog candidato.
- Seleção Brasileira 1978: continua sem coleção.
- Atlético-MG 1979 (`10-12/1979-ae6fca`): o candidato conservador remove a coleção e produziria rota provisória sem coleção.

As três rotas oficiais continuam HTTP 200 porque nenhuma camada oficial foi alterada. Não existe mecanismo geral de alias/redirect para rotas de item. O risco do link Atlético-MG é significativo e constitui gate FAIL. Nenhum frontend foi alterado.

## 18. Mídias

O candidato gerou as mesmas 16.245 relações históricas declaradas pelo run 10, mas o Catalog oficial atual contém zero linhas reais. Não houve movimentação, cópia, renomeação ou exclusão física. A comparação pública definitiva exigiria View/Media candidatos, proibidos nesta ET.

## 19. Duplicações

- itens: 4.465 chaves únicas;
- relações: todas apontam para itens candidatos existentes;
- slugs-base Catalog: sem mudança;
- colisões em rotas provisórias: zero;
- itens por equipe: invariantes.

Não houve duplicação no candidato.

## 20. fot-gio

Atual: Torino `fot_gio` possui 11 itens Catalog; View anuncia 11/33; API detalhe retorna zero. Candidato: Torino `fot_gio` teria 4 itens, pois referências cross-team de Roma são bloqueadas. Embora tecnicamente mais conservador, isso altera explicitamente o caso fora de escopo. Gate: FAIL.

## 21. catalog_item_images

Atual oficial: 0. Candidato: 16.245. O mecanismo normal do Catalog inevitavelmente popula a tabela. A ET determina parar antes da persistência nessa situação. Gate: FAIL.

## 22. MEDIA_ONLY

14/14 continuam vazias no candidato. Gate: PASS.

## 23. LEGITIMATELY_EMPTY

2/2 continuam vazias no candidato. Gate: PASS.

## 24. Oito itens sem mídia

Estado público oficial: 8 antes e 8 depois. Não foi possível produzir a métrica pública candidata sem reconstruir View/Media, ação proibida. Nenhuma mídia oficial foi alterada.

## 25. Pre-flight gate

| Critério | Resultado |
|---|---|
| Catalog tests | PASS — 16/16 |
| 4.465 itens | PASS |
| Zero duplicação | PASS |
| Zero mudança de equipe | PASS |
| 703 exclusivos | PASS — 703/703 |
| 217 mistos protegidos | PASS — 217/217 |
| MEDIA_ONLY | PASS — 14/14 |
| LEGITIMATELY_EMPTY | PASS — 2/2 |
| Snapshot/rollback | PASS |
| 8 itens sem mídia oficiais | PASS — 8/8 |
| Somente 703 reassociações | **FAIL — 1.239** |
| Collections becoming empty seguras | **FAIL — 30 não comprovadas** |
| fot-gio intacto | **FAIL — 11→4** |
| `catalog_item_images` intacta | **FAIL — 0→16.245** |
| Link Atlético-MG/Chicão | **FAIL — rota candidata muda** |
| Substituição isolada do Catalog | **FAIL — FK impede `replace_previous=True`** |

Resultado global: **REPROVADO**.

## 26. Persistência executada ou bloqueada

Bloqueada antes de qualquer escrita no banco oficial. Não houve tentativa no arquivo oficial. O run 11 existe somente na cópia candidata descartável.

## 27. Estado pós-Catalog

Não aplicável ao oficial: Catalog run 10 continua ativo. Normalization 9, View 15, Media 17 e Historical Collections permanecem sem rebuild.

## 28. Testes

- Catalog antes do preflight: 16/16 PASS.
- O preflight usou o pipeline oficial em cópia SQLite íntegra.
- Backend completo: 122/122 PASS, com uma advertência Starlette.
- Frontend nomes: 6/6 PASS; busca: 11/11 PASS.
- Lint e build: PASS.

## 29. HTTP

12/12 rotas verificadas responderam HTTP 200: `/site`, `/site/paises`, `/site/equipes`, `/site/colecoes`, `/site/ultimas`, `/site/chicao`, três amostras de catálogo e as três camisas do Chicão.

## 30. Integridade

O banco oficial manteve tamanho, timestamp, métricas e máximos de run. Nenhuma camada oficial foi reconstruída ou substituída.

## 31. Arquivos criados

- `database/snapshots/et-029b-preflight-20260820.db`;
- `docs/et-029b-item-route-mapping.csv`;
- `docs/et-029b-exclusive-record-recovery.md`.

## 32. Arquivos alterados

Nenhum arquivo funcional foi alterado nesta ET.

## 33. Arquivos removidos

A cópia temporária `database/snapshots/et-029b-candidate-20260820.db` foi removida após a validação final; não era snapshot de rollback nem artefato de entrega.

## 34. Limitações

- Normalization/View/Media candidatos não foram reconstruídos devido aos gates e às proibições.
- Rotas candidatas usam slugs públicos atuais e são explicitamente provisórias.
- Os 536 reassociados adicionais precisam de classificação formal antes de futura autorização.
- As 30 coleções esvaziadas precisam de auditoria histórica individual.

## 35. Próxima recomendação

Não autorizar nova persistência ainda. Primeiro separar uma mudança de pipeline transacional que trate `catalog_item_images` e dependências, classificar os 536 registros adicionais, auditar as 30 coleções, decidir `fot-gio` e proteger a rota memorial do Atlético-MG. Nenhuma próxima ET foi iniciada.
