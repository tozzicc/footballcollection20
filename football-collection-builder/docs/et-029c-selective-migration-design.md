# ET-029C — Desenho e validação da migração seletiva dos 703 registros

## 1. Resumo executivo

**Decisão: `OPTION_C_BLOCKED_PENDING_NEW_AUTHORIZATION`.** A atualização seletiva de `catalog_items.collection_id` é tecnicamente transacional e preserva IDs, identidade, slugs, equipes, contagens, mídia e FKs. Em cópia temporária, os 703 movimentos recuperaram 263 coleções e não esvaziaram nenhuma coleção. A aplicação oficial, porém, não é segura no escopo atual: cinco itens autorizados saem de `Torino/fot_gio` (11→6), 703 stable keys passam a ser semanticamente incompatíveis com o novo pai e Normalization/View permanecem materialmente desatualizadas. Nenhuma escrita ocorreu no banco oficial.

## 2. Escopo e baseline preservado

Fonte primária: `docs/et-029b-item-route-mapping.csv`. Universo fechado: 703 linhas `EXCLUSIVE + REASSOCIATE`; os 536 `OTHER + REASSOCIATE`, 217 `MIXED`, 572 `OTHER + BLOCKED_AMBIGUOUS` e 106 `BLOCKED_CROSS_TEAM` ficaram fora.

Baseline oficial: 3 países, 175 equipes, 930 coleções, 4.465 itens, 351 coleções públicas vazias, 8 itens ready sem mídia, zero `catalog_item_images` e 16.417 relações de mídia na View. Runs: HTML 3, Image 2, Catalog 10, Quality 7, Normalization 9, View 15 e Media 17.

## 3. Revisão histórica incorporada

Foram preservadas as decisões de ET-022R/023/023A (nomes somente editoriais), ET-024A–E (rotas memoriais), ET-025 (contrato público), ET-026–026C (busca contextual/exata), ET-027 (classes de coleções vazias), ET-028 (703 exclusivos e 217 mistos), ET-029A (associação por registro) e ET-029B (gates de escopo, `fot-gio`, mídia e dependências).

## 4. Modelo relacional e FKs

- `catalog_items.collection_id → catalog_collections.id`, `ON DELETE SET NULL`;
- `catalog_items.team_id → catalog_teams.id`, `ON DELETE CASCADE`;
- `catalog_item_images.catalog_item_id → catalog_items.id`, `ON DELETE CASCADE`;
- Quality referencia o Catalog run 10; issues usam `entity_id` lógico;
- Normalization run 9 referencia Catalog 10 com `ON DELETE RESTRICT`;
- `catalog_normalized_items.source_entity_id` e `collection_stable_key` são referências lógicas, sem FK ao Catalog;
- View 15 referencia Normalization 9 com `ON DELETE RESTRICT`;
- Media 17 referencia View 15 com `ON DELETE RESTRICT`.

A troca isolada de `collection_id` passa nas FKs porque o item e a coleção continuam existentes, mas não atualiza automaticamente stable keys nem projeções derivadas.

## 5. Identidade: IDs, stable keys e slugs

- IDs dos 4.465 itens: preserváveis e preservados no protótipo;
- `relative_path`, `team_id` e slug-base do Catalog: preserváveis e preservados;
- slugs públicos atuais: 0/703 mudanças no preflight;
- stable keys físicas: preserváveis, mas **não semanticamente válidas** depois da troca de pai; 703/703 diferem da stable key candidata calculada pelo builder;
- rotas: 703/703 mudariam o segmento de coleção quando as camadas públicas fossem propagadas.

Portanto, “preservar stable key” e “refletir a associação correta” são requisitos incompatíveis sob a fórmula atual, que incorpora a coleção-pai.

## 6. Lista auditável

`docs/et-029c-authorized-703.csv` contém exatamente 703 IDs únicos com identidade, equipe, coleção atual, coleção-alvo, stable key, slug e rotas antes/alvo. Ela é a única whitelist aceita pelo protótipo.

## 7. Amostra controlada

Foram aplicados 20 movimentos em cópia temporária, cobrindo 6 equipes: Atlético-MG e Grêmio (Brasil), Juventus e Torino (Itália), Venezuela (Outros) e Corinthians. Resultado: 20/20 atualizados; zero item novo/excluído; IDs, equipes, paths e slugs preservados; `integrity_check=ok`; zero violações de FK. A cópia foi descartada.

## 8. Ensaio integral dos 703

Em segunda cópia temporária: 703/703 `collection_id` alterados, 0 já aplicados, 4.465 itens preservados, totais por equipe idênticos, identidades idênticas, zero `catalog_item_images`, `integrity_check=ok` e zero violações de FK. A cópia foi descartada.

## 9. Coleções recuperadas e remanescentes

- recuperadas: **263** (Brasil 136, Itália 123, Outros 4);
- vazias no Catalog após reassociação seletiva: **88**;
- não vazias: **842**;
- coleções anteriormente preenchidas que ficam vazias: **0**.

As 30 coleções que esvaziavam no rebuild global não esvaziam na estratégia seletiva, pois os 536 extras e os registros bloqueados não são movimentados.

## 10. MEDIA_ONLY e LEGITIMATELY_EMPTY

As 14 `MEDIA_ONLY` e 2 `LEGITIMATELY_EMPTY` permanecem fora da whitelist e vazias. A migração não tenta convertê-las em parser gap nem criar itens.

## 11. Os 536 extras

Os 536 são `OTHER`, todos já associados e apontam para 149 coleções atualmente preenchidas, em 25 equipes: Itália 378, Brasil 157 e Outros 1. Eles não pertencem ao conjunto ET-028 de diretórios parser/catalog gap e não são “resíduo inevitável” da recuperação dos 703. São uma população separada, originada pela aplicação global da nova regra a registros já materializados, e exigem classificação/autorização própria.

## 12. Proteção dos 217 mistos

217/217 não aparecem na whitelist e não foram tocados. Nenhuma heurística de primeiro candidato, fuzzy matching ou desempate foi adicionada.

## 13. `fot-gio`

Cinco dos 703 itens têm `collection_before=camisas/italia/torino/fot_gio`; nenhum tem `fot_gio` como alvo. Assim, a migração seletiva integral produz 11→6 (o rebuild global produziria 11→4). Isso viola a proteção herdada da ET-029B. O script bloqueia esse caso por padrão; existe override explícito apenas para ensaio em cópia e ele não autoriza aplicação oficial.

## 14. Chicão

- São Paulo 1977, rota `fot-gio/1977-5336f6`: fora da whitelist, preservada;
- Seleção Brasileira 1978, rota sem coleção: fora da whitelist, preservada;
- Atlético-MG 1979, rota `10-12/1979-ae6fca`: registro 42421 é `OTHER/BLOCKED_AMBIGUOUS`, fora da whitelist, preservado.

Outros registros editoriais de 1979 podem estar nos 703, mas o registro efetivamente usado pelo memorial não muda. As três rotas responderam HTTP 200.

## 15. `catalog_item_images` e mídia

Permaneceu em zero no ensaio. Como somente `catalog_items.collection_id` foi atualizado, nenhum asset, relação, ordem ou caminho físico foi criado, movido, renomeado ou excluído. As 16.417 relações públicas da View permaneceram intactas e antigas.

## 16. Oito itens sem mídia

Continuam 8 na View oficial. O protótipo não altera a View nem mídia; portanto, não cria nem resolve falta de mídia. Uma futura propagação deve repetir esse gate.

## 17. Quality

Quality 7 continua tecnicamente íntegra e ligada ao Catalog 10. Nenhum dos 703 itens possui issue de item no run atual. Ainda assim, a avaliação é anterior à reassociação e deve ser revalidada antes de publicação.

## 18. Normalization

Há 703/703 itens correspondentes em Normalization 9. Seus `source_entity_id` continuam válidos, mas `stable_key` e `collection_stable_key` permanecem representando a coleção antiga. Estado: tecnicamente íntegro, semanticamente desatualizado.

## 19. View

View 15 permanece consultável e com rotas antigas, mas não reflete as 263 coleções recuperadas nem os 703 novos vínculos. Estado: tecnicamente íntegro, semanticamente desatualizado. Publicar após alterar apenas o Catalog geraria divergência entre API pública e fonte Catalog.

## 20. Estratégia de rebuild/propagação

Não é seguro reconstruir o Catalog globalmente. Uma futura ET deve: (1) decidir os cinco `fot_gio`; (2) decidir política de stable key/aliases; (3) atualizar seletivamente o Catalog em transação; (4) executar Quality; (5) reconstruir ou propagar Normalization, View e Media de modo controlado; (6) criar redirects/aliases para as 703 rotas antigas, se as rotas novas forem publicadas; (7) repetir os gates Chicão, busca e mídia. Nenhuma dessas etapas dependentes foi executada aqui.

## 21. Protótipo de migração

`scripts/migrations/et_029c_selective_collection_reassociation.py`:

- dry-run por padrão e rollback ao fim;
- `--database` e `--authorized-csv` obrigatórios;
- recusa absoluta do caminho da base oficial;
- `--apply` explícito somente para cópia;
- baseline Catalog 10/4.465 e whitelist com 703 linhas/IDs únicos;
- valida identidade, equipe, stable key, slug, origem e alvo;
- bloqueia alvo cross-team, divergência e `fot_gio` sem override explícito;
- uma única transação e rollback em qualquer falha;
- idempotente quando todos os itens já estão no alvo;
- valida contagem, identidade, `catalog_item_images`, integridade e FKs.

## 22. Testes do protótipo

9/9 PASS: dry-run/rollback, apply, idempotência, preservação de identidade, divergência de stable key/equipe/identidade, alvo ausente/cross-team, `fot_gio`, cardinalidade da whitelist e recusa do banco oficial.

## 23. Testes gerais

- backend completo: **131/131 PASS** (uma advertência de depreciação Starlette);
- nomes públicos: **6/6 PASS**;
- busca pública: **11/11 PASS**;
- lint: PASS;
- build: PASS fora do sandbox; a primeira tentativa foi bloqueada pelo carregamento nativo Tailwind/Vite (`EPERM`), sem falha de código.

## 24. HTTP e busca

HTTP 200 em 6 páginas públicas, health, países, buscas Juventus/Atlético/Chicão e nas três rotas de camisas do Chicão. Nenhuma resposta usa o banco temporário; isso valida que o contrato oficial permaneceu estável.

## 25. Integridade e duplicação

Nas cópias: `PRAGMA integrity_check=ok`, `foreign_key_check=0`, 4.465 itens, zero alteração de equipe, zero item duplicado/novo/excluído, zero alteração física de mídia. A identidade técnica foi preservada integralmente.

## 26. Aplicação oficial

**Não executada.** Nenhum run oficial foi criado ou substituído. Nenhum rebuild de Catalog, Quality, Normalization, View, Media ou Historical Collections foi realizado.

## 27. Rollback real

Não foi necessário porque as únicas aplicações ocorreram em diretórios temporários automaticamente descartados. O dry-run do script executa as validações dentro de transação e sempre faz rollback.

## 28. Arquivos criados

- `docs/et-029c-authorized-703.csv`;
- `docs/et-029c-selective-migration-design.md`;
- `scripts/migrations/et_029c_selective_collection_reassociation.py`;
- `backend/tests/test_et029c_selective_migration.py`.

## 29. Arquivos alterados/removidos

Nenhum arquivo funcional preexistente foi alterado. Nenhum arquivo oficial foi removido. As duas cópias SQLite e a whitelist de amostra foram temporárias e descartadas.

## 30. Limitações e decisão final

O ensaio prova que a técnica seletiva elimina os 536 extras e as 30 coleções esvaziadas, mas não resolve três decisões de produto/dados: cinco saídas de `fot_gio`, regeneração de 703 stable keys/camadas derivadas e compatibilidade das 703 rotas antigas. Logo, a migração oficial fica bloqueada até autorização explícita e desenho da propagação dependente.

**Decisão final: `OPTION_C_BLOCKED_PENDING_NEW_AUTHORIZATION`.**
