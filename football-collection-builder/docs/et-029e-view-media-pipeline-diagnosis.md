# ET-029E — Diagnóstico do pipeline View/Media

## 1. Resumo executivo

**Decisão: `OPTION_B_CODE_FIXED_BUT_MORE_VALIDATION_REQUIRED`.** Não existia item perdido: Catalog, Normalization e View candidatos contêm 4.465 itens. O número 4.464 era a quantidade de itens `ready` sem mídia no View incompleto. A perda de mídia foi reproduzida e corrigida estruturalmente no candidato: o Image Parser run 2 apagou `image_metadata` antigo e o `ON DELETE CASCADE` removeu 16.245 linhas de `catalog_item_images`. Com as relações recompostas a partir do parser atual, o pipeline temporário produziu 16.245 relações Catalog, 16.417 View e 16.618 Media, exatamente como o estado histórico esperado.

O candidato ainda não atende literalmente `zero cross-team`: preserva 24 anomalias já existentes no baseline, cinco delas protegidas por `fot_gio`, embora introduza zero novas. A próxima autorização deve aceitar explicitamente esse baseline ou tratar os casos, atualmente fora de escopo.

## 2. Baseline oficial

Catalog 10, Normalization 9, View 15, Media 17 e Historical Collections 1; 3 países, 175 equipes, 930 coleções, 4.465 itens, 351 coleções vazias, 8 itens sem mídia e zero linhas atuais em `catalog_item_images`. Nenhum run oficial foi alterado.

## 3. Estado candidato ET-029D

698 reassociações seguras; 4.465 itens; 91 coleções vazias; 260 recuperadas; zero esvaziadas; `fot_gio=11`; 536 extras e 217 mistos intactos. A reconstrução incompleta gerava 172 relações View porque a fonte Catalog de mídia estava vazia.

## 4. O suposto item perdido

Não há item ausente. O diff integral mostrou:

| Etapa | Esperado | Encontrado | Ausentes |
|---|---:|---:|---:|
| Catalog candidato | 4.465 | 4.465 | 0 |
| Normalization candidata | 4.465 | 4.465 | 0 |
| View candidata | 4.465 | 4.465 | 0 |

O arquivo `docs/et-029e-missing-item-analysis.csv` registra a reconciliação.

## 5. Causa da aparente perda

Classificação: `OTHER / METRIC_MISINTERPRETATION`. A consulta ET-029D contou `public_status='ready' AND images_count=0`, cujo resultado era 4.464 antes da restauração de mídia. Esse valor não era `COUNT(catalog_view_items)`. Nenhum filtro, dedup, colisão ou status removeu item entre as camadas.

## 6. Correção do item

Nenhuma correção foi aplicada a Normalization ou View porque não havia bug de perda de item. Criar item artificial ou alterar filtros seria incorreto.

## 7. Pipeline real de mídia

Fluxo comprovado:

`inventory/html_image_references/html_image_contexts` → Image Parser (`image_metadata`) → Catalog Builder (`catalog_item_images`) → View Builder (`catalog_view_media`) → Media Builder (`media_asset_relations`/`media_assets`) → API/frontend.

Normalization não transporta mídia; mantém a identidade normalizada usada pelo View. Team/Country Branding e Historical Collections acrescentam relações fora das relações de itens.

## 8. Função de `catalog_item_images`

A tabela materializa a relação entre `catalog_items` e `image_metadata`, guardando página, referência original, path, ordem, alt e candidato primário. FKs: build→Catalog run, item→Catalog item e imagem→Image Metadata, todas com cascade. Normalization não a consome. O `CatalogViewRepository.load_source()` a consome pelo Catalog build da Normalization. O View a transforma em mídia pública; o Media Builder resolve os paths e disponibilidade.

## 9. Causa das 172 relações

As 172 sobreviventes são branding de equipes e países, carregado de `team_branding` e `country_branding`. Nenhuma era relação de item. Assim, 16.245 relações de item ausentes + 172 branding = 172 no View incompleto; após correção, 16.245 + 172 = 16.417.

## 10. Ponto exato da perda

O Catalog 10 terminou às 16:11 com `image_relations=16.245`. O Image Parser run 2 executou às 21:02 com `replace_previous=True`. `ImageParserRepository.save_run()` apagou as tabelas antigas; a exclusão de `image_metadata` acionou `catalog_item_images.image_metadata_id ON DELETE CASCADE`. O contador do run 10 ficou histórico, mas as linhas reais foram removidas.

## 11. Sequenciamento correto

Ordem segura: Inventory/HTML Parser → Image Parser → Catalog e relações → Quality → Normalization → View → Media. Um novo Image Parser depois do Catalog deve bloquear ou exigir rebuild coordenado das relações antes de View/Media. Construir View a partir de `catalog_item_images=0` é fonte incompleta.

## 12. Correções aplicadas

1. `ImageParserRepository.save_run()` agora bloqueia substituição quando existem relações Catalog dependentes, antes de qualquer cascade.
2. O script de migração ganhou `restore_catalog_image_relations()`: executa o Catalog Builder por um repositório somente-captura, exige o mesmo conjunto de 4.465 identidades, relaciona as referências aos IDs Catalog existentes, valida o Image run atual, duplicações e FKs, e materializa somente relações em cópia autorizada.

Nenhuma imagem foi criada, copiada, convertida, movida ou inferida.

## 13. Testes adicionados

Foi adicionado teste que reproduz uma relação Catalog dependente e comprova que a substituição do Image Parser falha antes de apagar `image_metadata`/`catalog_item_images`. O restaurador foi validado no snapshot integral em dry-run/aplicação temporária, inclusive cardinalidade, identidades, múltiplas mídias, ordem, duplicações e FKs.

Testes finais: backend completo **133/133 PASS**; frontend nomes **6/6**; busca **11/11**; lint PASS; build PASS. As seis páginas públicas e as três rotas memoriais responderam HTTP 200 no estado oficial preservado.

## 14. Pipeline candidato completo

Em cópia temporária: migração dos 698 → restauração das 16.245 relações → recálculo das 698 stable keys → Normalization 10 temporária → View 16 temporário → Media 18 temporário. A cópia foi descartada após as verificações.

## 15. Catalog

4.465 itens, 930 coleções, 16.245 relações, 4.457 itens com relação e 8 sem relação. IDs e equipes preservados; 698 `collection_id` alterados; zero item novo/excluído.

## 16. Normalization

4.465 itens. As 698 stable keys, collection keys e slugs foram recalculadas; os demais itens permaneceram estáveis. Zero stable key duplicada.

## 17. View

4.465 itens, 930 coleções, 16.417 relações, 4.465 rotas únicas. Agrupamento: 91 coleções vazias e 839 preenchidas. Breadcrumbs e collection slugs refletem o candidato.

## 18. Media

Media temporário: 16.618 relações totais, 15.592 assets únicos, disponíveis e válidos. A diferença 16.618−16.417 corresponde às relações adicionais já incorporadas pelo Media Repository, incluindo coleções históricas. As contagens coincidem com Media 17; não há perda inexplicada.

## 19. As 698 reassociações

698/698 foram aplicadas somente na cópia. Todas mantiveram equipe e item, receberam coleção determinística e preservaram mídia. O mapa final está em `docs/et-029e-final-route-impact.csv`.

## 20. Os 536 extras

536/536 associações, stable keys, slugs e equipes permaneceram intactas.

## 21. Os 217 mistos

217/217 permaneceram intactos e sem associação automática nova.

## 22. `fot_gio`

Permaneceu com 11 itens. Os cinco casos Roma→Torino continuaram excluídos, conforme ET-029D.

## 23. As 30 coleções

30/30 coleções que esvaziavam no rebuild global permaneceram preenchidas; zero coleção preenchida ficou vazia.

## 24. MEDIA_ONLY

14/14 permaneceram vazias e intocadas.

## 25. LEGITIMATELY_EMPTY

2/2 permaneceram vazias e intocadas.

## 26. Itens sem mídia

- com mídia: 4.457;
- sem mídia: 8;
- uma mídia: 317;
- duas mídias: 640;
- três ou mais: 3.500;
- `PRESERVED`: 8;
- `RECOVERED_WITH_MEDIA`: 0;
- `NEW_MISSING_MEDIA`: 0.

Os oito estão listados em `docs/et-029e-media-diff.csv`; nenhum pertence aos 698.

## 27. Rotas

698 rotas mudam em coleção e slug, como previsto; equipe, coleção, item e mídia estão corretos. Zero colisão. Nenhuma rota oficial foi alterada nesta ET.

## 28. Chicão

São Paulo 1977, Seleção Brasileira 1978 e Atlético-MG 1979 ficaram fora dos 698 e preservam seus destinos atuais. As três rotas oficiais continuaram HTTP 200.

## 29. Integridade

No candidato: `integrity_check=ok`, `foreign_key_check=0`, zero stable key duplicada, zero rota duplicada, zero relação Media duplicada indevida e zero cross-team **novo**. O total cross-team permaneceu 24→24 por anomalias do baseline que esta ET proíbe corrigir.

## 30. Riscos restantes

- o critério literal `zero cross-team` conflita com a obrigação de preservar `fot_gio` e demais casos fora de escopo;
- o fluxo futuro precisa coordenar Catalog/relações/Quality/Normalization/View/Media e rollback como uma operação auditável;
- 698 rotas necessitam política de compatibilidade/redirect;
- o restaurador foi comprovado no snapshot integral, mas ainda não foi executado oficialmente.

## 31. Decisão final

`OPTION_B_CODE_FIXED_BUT_MORE_VALIDATION_REQUIRED`. O problema View/Media está corrigido e o pipeline numérico fecha integralmente, mas `OPTION_A` exige zero cross-team absoluto. O candidato preserva 24 casos preexistentes por exigência de escopo. É necessária decisão explícita sobre aceitar `zero novos cross-team` como gate ou autorizar auditoria/correção dos 24.

## 32. Plano objetivo para a próxima ET

Autorizar explicitamente uma das alternativas: (a) aceitar baseline 24 e exigir zero novos; ou (b) auditar/corrigir os 24 antes da aplicação. Depois executar em snapshot validado uma transação/orquestração coordenada: 698 → relações → Quality → Normalization → View → Media → gates → troca oficial/rollback. Nenhuma próxima ET foi iniciada.

## 33. Integridade oficial

Banco oficial permaneceu com Catalog 10, Normalization 9, View 15, Media 17, 4.465 itens e `catalog_item_images=0`; tamanho 445.566.976 bytes, `mtime_ns=1787141730427370700`, `integrity_check=ok` e zero violações de FK. Nenhuma camada oficial foi reconstruída ou substituída. Nenhum commit ou push foi realizado.
