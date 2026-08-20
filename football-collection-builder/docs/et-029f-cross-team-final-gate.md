# ET-029F — Auditoria cross-team e gate final

## 1. Resumo executivo

**Decisão: `OPTION_A_GATE_APPROVED_FOR_ET029G`.** As 24 anomalias cross-team são integralmente preexistentes, aparecem com os mesmos IDs e vínculos no snapshot ET-029B e no Catalog oficial 10, ficam fora dos 698 e permanecem 24→24 no pipeline candidato. Resultado: `NEW=0`, `WORSENED=0`, `RESOLVED=0`, `UNCHANGED=24`. Nenhuma bloqueia tecnicamente a recuperação das 260 coleções. O gate correto é baseado em zero anomalias novas/pioradas e inventário completo do baseline, não em total absoluto zero.

## 2. Baseline

Oficial: Catalog 10, Normalization 9, View 15, Media 17, Historical Collections 1; 3 países, 175 equipes, 930 coleções, 4.465 itens, 351 coleções vazias, 8 itens sem mídia e `catalog_item_images=0`. Cross-team Catalog: 24.

## 3. Objetivo

Auditar 24/24 sem corrigi-las, provar preexistência, comparar antes/depois do pipeline ET-029E e definir o gate operacional da futura ET-029G. Nenhuma aplicação oficial foi executada.

## 4. As 24 anomalias

O inventário completo está em `docs/et-029f-cross-team-anomalies.csv`. Distribuição estrutural:

- Roma item → Torino `fot_gio`: 11;
- páginas de América-RN, Internacional de Limeira, Mirassol, Rio Claro, Israel e Macedônia → Sport `07_17`: 6;
- páginas de Alzano Virescit, Jrcasale, Monza, Torres e Treviso → Ternana `08_16`: 5;
- Salernitana → Querétaro `07_17`: 1;
- Suécia → Manchester City `06_18`: 1.

Todas as 24 rotas atuais responderam HTTP 200.

## 5. Evidência de preexistência

24/24 constam no Catalog run 10 oficial e no snapshot `et-029b-preflight-20260820.db`, com o mesmo item ID e mismatch item-team/collection-team. Normalization 9 mantém seus `source_entity_id` e stable keys; View 15 expõe suas rotas e mídia. Todas também aparecem no mapa ET-029B. Classificação de evidência: `CONFIRMED_PREEXISTING=24`, `NOT_CONFIRMED_PREEXISTING=0`.

## 6. Classificação

- **E — SOURCE_PAGE_CROSS_TEAM: 13.** A página fica sob uma equipe, mas seu grupo editorial resolve imagens de outra equipe/coleção; o Catalog antigo associou a coleção referenciada apesar do team do item.
- **F — KNOWN_SPECIAL_CASE: 11.** Itens Roma associados à coleção protegida Torino/`fot_gio`, caso já isolado nas ET-029B–D.
- A/B/C/D/G: 0 como categoria principal. Todos materializam tecnicamente um `COLLECTION_TEAM_MISMATCH`, mas E/F explicam melhor a origem documental.

## 7. Risco

- LOW: 0;
- MEDIUM: 11 (`fot_gio`, funcional e conhecido, mas semanticamente inconsistente);
- HIGH: 13 (conteúdo de outra equipe pode aparecer sob team segment incorreto);
- CRITICAL: 0.

Os 13 HIGH são dívida técnica relevante, mas não são regressão do candidato e suas rotas/mídia permanecem funcionais.

## 8. Relação com os 698

- dentro dos 698: 0;
- entre os 536 extras: 1 (item 45782, Roma);
- entre os 217 mistos: 1 (item 45775, Roma);
- cinco `EXCLUSIVE` são precisamente os excluídos `fot_gio` da ET-029D;
- os demais estão em populações bloqueadas/fora da whitelist.

Nenhum dos 24 recebe update de `collection_id`, stable key, slug ou rota pela migração dos 698.

## 9. Antes/depois

Para 24/24: item ID, team, collection, stable key, slug, rota, mídia e status público permanecem iguais. Classificação comparativa: `UNCHANGED=24`; `CHANGED_BUT_SAME_PREEXISTING_ANOMALY=0`; `WORSENED=0`; `RESOLVED_INCIDENTALLY=0`.

## 10. Novas anomalias

Comparação integral dos 4.465 itens: `CROSS_TEAM_BEFORE=24`, `CROSS_TEAM_AFTER=24`, `PREEXISTING=24`, `NEW=0`.

## 11. Worsened

Zero. Nenhum par item-team/collection-team preexistente mudou e nenhuma rota ou mídia das 24 piorou.

## 12. Resolvidas incidentalmente

Zero. O pipeline não foi modificado para corrigir casos fora do escopo.

## 13. `fot_gio`

11 itens antes e 11 no candidato. Os 11 itens Roma→Torino permanecem cross-team conhecidos; cinco registros exclusivos continuam explicitamente excluídos. Não houve perda, reassociação ou mudança causada pelos 698.

## 14. Pipeline ET-029E

Reproduzido integralmente em nova cópia temporária: 698 seletivos → 16.245 relações Catalog restauradas → stable keys → Normalization → View → Media. A cópia foi descartada.

## 15. Coleções

930 totais; vazias 351→91; recuperadas 260; preenchidas esvaziadas 0. As 30 coleções protegidas permanecem preenchidas. Os 536 extras e 217 mistos permanecem intactos. As 14 MEDIA_ONLY e 2 LEGITIMATELY_EMPTY continuam vazias.

## 16. Mídias

- Catalog: 16.245 relações;
- View: 16.417;
- Media: 16.618;
- assets únicos/disponíveis: 15.592;
- duplicações indevidas: zero.

## 17. Itens sem mídia

4.457 itens com mídia e os mesmos 8 sem mídia; `NEW_MISSING_MEDIA=0`.

## 18. Rotas

698 rotas mudam semanticamente, com team segment e collection segment corretos para a whitelist. Zero rota duplicada, zero stable key duplicada e zero cross-team novo.

## 19. Chicão

São Paulo 1977, Seleção Brasileira 1978 e Atlético-MG 1979 ficam fora dos 698 e das mudanças cross-team. As três rotas oficiais continuam HTTP 200 e seus destinos candidatos permanecem iguais.

## 20. Gate antigo

`cross_team_total == 0` é incompatível com o baseline oficial e com a proteção explícita de `fot_gio`. Ele mede dívida histórica, não regressão da migração autorizada.

## 21. Gate proposto

Gate aprovado:

```text
cross_team_new == 0
AND cross_team_worsened == 0
AND cross_team_total == 24
AND all_preexisting_cross_team_are_accounted_for == true
```

Qualquer alteração de ID, team, collection, rota, mídia ou status dos 24 deve falhar a aplicação, salvo autorização futura específica.

## 22. Riscos de publicação

Nenhuma das 24 bloqueia tecnicamente ET-029G: todas são preexistentes, funcionais, fora dos 698 e invariantes. O risco editorial dos 13 casos HIGH permanece visível, mas não é causado nem agravado pela recuperação das coleções.

## 23. Dívida técnica pós-V1

Abrir frente separada, após publicação, para os 13 source-page cross-team e 11 Roma/`fot_gio`. A auditoria futura deve decidir team editorial, collection correta, redirects e impacto histórico sem aproveitar incidentalmente o pipeline dos 698.

## 24. Decisão final

`OPTION_A_GATE_APPROVED_FOR_ET029G`. Requisitos atendidos: 24/24 comprovadas; NEW=0; WORSENED=0; pipeline completo reproduzido; nenhuma anomalia bloqueia a recuperação; demais gates ET-029E permanecem aprovados.

## 25. Gate operacional para ET-029G

Pré-apply:

- snapshot íntegro e rollback testado;
- runs oficiais 10/9/15/17;
- 4.465 itens, 930 coleções, 351 vazias;
- whitelist exatamente 698 e exclusões `fot_gio` exatamente 5;
- 536 extras e 217 mistos congelados;
- lista cross-team exatamente igual ao CSV de 24 IDs/pares;
- banco sem escrita concorrente.

Durante:

- uma operação coordenada e auditável para Catalog/relações/Quality/Normalization/View/Media;
- rollback integral em qualquer divergência;
- nenhuma atualização fora da whitelist;
- nenhuma imagem criada/movida/renomeada.

Pós-apply:

- Catalog/Normalization/View: 4.465;
- coleções vazias 91; recuperadas 260; esvaziadas 0;
- relações 16.245/16.417/16.618 e assets 15.592;
- itens sem mídia 8;
- `fot_gio=11`;
- cross-team total 24, NEW=0, WORSENED=0 e 24/24 invariantes;
- zero colisões/duplicações;
- `integrity_check=ok`, `foreign_key_check=0`;
- Chicão, busca e HTTP aprovados antes da troca definitiva.

## 26. Testes

Backend completo **133/133 PASS**; nomes **6/6**; busca **11/11**; lint e build PASS. Nenhum código funcional foi alterado nesta ET e nenhum teste artificial foi criado.

## 27. HTTP

Validação no estado oficial ativo: seis páginas públicas, seis buscas protegidas, três rotas memoriais (**15/15**) e as 24 rotas cross-team responderam HTTP 200.

## 28. Integridade oficial

Banco oficial permaneceu somente leitura, com Catalog 10, Normalization 9, View 15 e Media 17; 445.566.976 bytes e `mtime_ns=1787141730427370700`. `integrity_check=ok`, zero violações de FK, 4.465 itens e `catalog_item_images=0`.

## 29. Arquivos criados/alterados

Criados: `docs/et-029f-cross-team-final-gate.md` e `docs/et-029f-cross-team-anomalies.csv`. Nenhum arquivo funcional foi alterado ou removido.

## 30. Próxima recomendação

ET-029G pode ser autorizada separadamente usando o gate operacional acima. Não aplicar automaticamente e não ampliar o escopo para corrigir as 24 anomalias.
