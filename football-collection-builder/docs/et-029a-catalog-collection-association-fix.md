# ET-029A — Correção controlada da associação item → coleção

## 1. Resumo executivo

A regra defeituosa do Catalog foi substituída por resolução determinística por `EditorialRecord`. Cada registro usa somente suas próprias referências. Um candidato único, existente e pertencente à mesma equipe é associado; zero candidatos, múltiplos candidatos ou candidato cross-team preservam o item sem coleção e com status seguro.

Nenhum build oficial foi executado. A validação usou testes, banco aberto em modo read-only e persistência capturada em memória. A amostra real teve 25 registros exclusivos, 6 equipes e resultado 25 PASS / 0 FAIL / 0 AMBIGUOUS.

## 2. Baseline

| Métrica oficial | Antes | Depois |
|---|---:|---:|
| Países/regiões | 3 | 3 |
| Equipes | 175 | 175 |
| Coleções | 930 | 930 |
| Itens | 4.465 | 4.465 |
| Coleções vazias | 351 | 351 |
| Itens ready sem mídia | 8 | 8 |
| `catalog_item_images` | 0 | 0 |
| View media | 16.417 | 16.417 |

Runs oficiais preservados: HTML 3, Image 2, Catalog 10, Normalization 9, View 15 e Media 17.

## 3. Causa raiz herdada da ET-028

O builder calculava `collection_key` uma vez por página, interrompendo no primeiro path reconhecido. Todos os registros editoriais derivados da página recebiam esse mesmo valor, ainda que suas referências apontassem para outras coleções.

## 4. Arquivo/função responsável

- Arquivo: `backend/app/services/catalog_builder_service.py`.
- Método afetado: `CatalogBuilderService.build()`.
- Trecho anterior: laço sobre `page_refs`, antes do laço sobre `records`, com `break` no primeiro candidato.
- Motivo: decisão page-scoped aplicada a entidades record-scoped.
- Nova função auditável: `resolve_record_collection()`.

## 5. Regra antiga

`page_refs → primeiro diretório de coleção existente → collection_key único → todos os records`.

O fallback também aceitava coleção de outra equipe, pois validava somente a existência da chave global.

## 6. Nova regra

Para cada registro:

1. ler apenas `record.references`;
2. extrair o candidato `camisas/país/equipe/coleção`;
3. manter somente candidatos existentes em `collections`;
4. associar apenas quando existe exatamente um candidato e seu team key coincide com o da página;
5. caso contrário, retornar sem `collection_key` e sem escolher o primeiro.

## 7. Evidências utilizadas

- `resolved_relative_path` persistido pelo HTML Parser;
- conjunto de referências do próprio grupo editorial;
- collection key existente no Catalog;
- team key da coleção e da página.

Não são usados ano, filename semelhante, fuzzy matching, IA, visão, quantidade de imagens ou hardcode.

## 8. Tratamento de ambiguidade

- zero candidatos: `unavailable`, item preservado sem coleção;
- mais de um candidato: `ambiguous`, item preservado sem coleção;
- candidato de outra equipe: `cross_team`, item preservado sem coleção;
- internamente, o registro fica `unsupported` ou `ambiguous`, impedindo publicação como associação segura.

## 9. Amostra controlada

Foram selecionados 25 registros exclusivos reais: Juventus 8, Atlético-MG 4, Palmeiras 4, Cagliari 4, Chievo Verona 4 e Venezuela 1. A amostra inclui Brasil, Itália e Outros, baixa/alta incidência e sete páginas com múltiplas coleções.

## 10. Tabela antes/depois da amostra

| # | Equipe | Página | Registro | Regra antiga | Esperado / nova regra | Resultado |
|---:|---|---|---|---|---|---|
| 1 | Juventus | `juventus/0001.htm` | `table-109` | `00-10` | `09_22` | PASS |
| 2 | Juventus | `juventus/0001.htm` | `table-498` | `00-10` | `06_18` | PASS |
| 3 | Juventus | `juventus/0304.htm` | `table-324` | `foto_juv` | `00-10` | PASS |
| 4 | Juventus | `juventus/0708.htm` | `table-266` | `00-10` | `foto_juv` | PASS |
| 5 | Juventus | `juventus/1011.htm` | `table-360` | `10_20` | `10_13` | PASS |
| 6 | Juventus | `juventus/1011.htm` | `table-392` | `10_20` | `00-10` | PASS |
| 7 | Juventus | `juventus/1314.htm` | `table-80` | `06_14` | `02_15` | PASS |
| 8 | Juventus | `juventus/1314.htm` | `table-126` | `06_14` | `08_14` | PASS |
| 9 | Atlético-MG | `atletico/1979.htm` | `table-65` | `10_12` | `02_17` | PASS |
| 10 | Atlético-MG | `atletico/1979.htm` | `table-83` | `10_12` | `04_21` | PASS |
| 11 | Atlético-MG | `atletico/1979.htm` | `table-101` | `10_12` | `04_16` | PASS |
| 12 | Atlético-MG | `atletico/1979.htm` | `table-135` | `10_12` | `11_17_2` | PASS |
| 13 | Palmeiras | `palmeiras/2012.htm` | `table-30` | `10_12` | `07_17` | PASS |
| 14 | Palmeiras | `palmeiras/2013.htm` | `table-30` | `07_17` | `04_14` | PASS |
| 15 | Palmeiras | `palmeiras/2013.htm` | `table-125` | `07_17` | `04_16` | PASS |
| 16 | Palmeiras | `palmeiras/2015.htm` | `table-30` | `01_16` | `06_16` | PASS |
| 17 | Cagliari | `cagliari/0203.htm` | `table-49` | `11_13` | `02_13` | PASS |
| 18 | Cagliari | `cagliari/0203.htm` | `table-69` | `11_13` | `03_15` | PASS |
| 19 | Cagliari | `cagliari/0304.htm` | `table-32` | `02_13` | `03_14_2` | PASS |
| 20 | Cagliari | `cagliari/0405.htm` | `table-51` | `02_13` | `11_13` | PASS |
| 21 | Chievo Verona | `chievo/1213.htm` | `table-34` | `01_14` | `03_14` | PASS |
| 22 | Chievo Verona | `chievo/1314.htm` | `table-34` | `01_14` | `03_14` | PASS |
| 23 | Chievo Verona | `chievo/1314.htm` | `table-57` | `01_14` | `06_14` | PASS |
| 24 | Chievo Verona | `chievo/1314.htm` | `table-149` | `01_14` | `06_14_2` | PASS |
| 25 | Venezuela | `venezuela/2015.htm` | `table-34` | `01_16` | `06_16` | PASS |

Todos possuem confiança HIGH: o esperado é o único diretório comum às referências do registro e coincide exatamente com o resultado da nova função.

## 11. Resultado da Juventus

8/8 PASS. Três páginas (`0001`, `1011`, `1314`) provaram múltiplos registros da mesma página associados independentemente a destinos diferentes.

## 12. Resultado das demais equipes

17/17 PASS: Atlético-MG 4, Palmeiras 4, Cagliari 4, Chievo Verona 4 e Venezuela 1.

## 13. Múltiplas coleções na mesma página

O caso mais forte foi `paises/brasil/atletico/1979.htm`: quatro registros antes concentrados em `10_12` passaram, isoladamente, a resolver `02_17`, `04_21`, `04_16` e `11_17_2`. O teste unitário obrigatório também reproduz uma página sintética A/B e exige A→A e B→B.

## 14. Testes automatizados

Foram adicionados 10 testes específicos cobrindo:

1. coleção única;
2. dois registros/duas coleções;
3. vários registros;
4. registro exclusivo;
5. ambiguidade;
6. ausência de evidência;
7. proteção contra fallback da primeira coleção;
8. cross-team/fot-gio;
9. ausência de duplicação;
10. determinismo e integração do builder.

Resultados:

- Catalog específico: 16/16;
- backend completo: 122/122, uma advertência Starlette;
- frontend nomes: 6/6;
- frontend busca: 11/11;
- total de testes automatizados: 139 aprovados;
- lint e build: aprovados;
- HTTP: 9/9 rotas verificadas com 200.

## 15. Risco de stable keys/IDs/slugs/rotas

- Stable key do item: muda na futura reassociação, pois o parent collection stable key participa do hash. Risco esperado/alto para referências internas antigas.
- ID: um rebuild substitutivo recria linhas; não deve ser tratado como identidade pública estável. Risco alto se consumidores usam ID.
- Slug: o título-base não muda, mas o novo escopo de coleção pode acionar `SL002`; risco médio e deve ser pré-calculado.
- Rota pública: muda intencionalmente o segmento da coleção; risco alto de quebra de links antigos sem redirects.
- Media URL/key: tende a permanecer pela identidade de mídia, mas a relação carrega a rota do item; risco médio até dry-run completo de Normalization/View/Media.

## 16. Risco de duplicação

O dry-run preservou 4.465 chaves de item únicas e 16.245 relações, todas apontando para records existentes. Nenhum item foi criado ou clonado. Ainda há risco de colisão de slug/rota após Normalization para registros que convergirem na mesma coleção; ET-029B deve bloquear publicação se qualquer colisão aparecer.

## 17. Impacto estimado para ET-029B

- 703 registros exclusivos continuam automaticamente recuperáveis.
- 217 registros mistos da população ET-028 permanecem fora da associação automática.
- Dry-run global: 4.465 itens preservados; 2.842 associados; 1.623 conservadoramente sem coleção; 812 coleções não vazias e 118 vazias no output descartável.
- A diferença de 118 para o mínimo teórico 88 mostra que a regra conservadora também retira associações ambíguas de coleções hoje preenchidas. ET-029B precisa revisar esse impacto antes de substituir o Catalog oficial.

## 18. Proteção fot-gio

Antes/depois oficial: Torino anuncia 11 itens/33 imagens, os itens continuam materializados como Roma e a API Torino continua HTTP 200 com total 0. No código novo, evidência Torino em página Roma retorna `cross_team` e não é associada automaticamente. Nenhuma correção oficial de fot-gio foi feita.

## 19. Estado catalog_item_images

Antes/depois oficial: 0. O dry-run descartável produziu 16.245 relações em memória, registradas separadamente e nunca persistidas.

## 20. Integridade antes/depois

Banco oficial manteve tamanho, timestamp, máximos de runs e todas as métricas do baseline. As 351 coleções vazias e os oito itens sem mídia permaneceram inalterados. MEDIA_ONLY e LEGITIMATELY_EMPTY não foram tratados.

## 21. Arquivos criados

- `docs/et-029a-catalog-collection-association-fix.md`.

## 22. Arquivos alterados

- `backend/app/services/catalog_builder_service.py`;
- `backend/tests/test_catalog_builder.py`.

## 23. Arquivos removidos

Nenhum.

## 24. Limitações

- Nenhum run de Normalization/View/Media foi simulado; impactos de slug/rota permanecem para preflight da ET-029B.
- O dry-run completo é propositalmente conservador e não resolve registros mistos.
- O estado oficial continua refletindo a regra antiga até autorização futura.

## 25. Recomendação objetiva para ET-029B

Antes de qualquer substituição oficial: executar pipeline integral em banco temporário; comparar stable keys, slugs, rotas e mídias; revisar os 1.623 registros sem coleção; validar redirects; bloquear cross-team e colisões; só então solicitar autorização explícita para rebuild oficial.

ET-029B não foi iniciada. Nenhuma recuperação em massa, commit ou push foi realizada.
