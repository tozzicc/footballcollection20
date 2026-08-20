# ET-026 — Correções funcionais pós-homologação da V1.0

## Resultado

A busca pública agora combina os resultados da API com as 175 equipes e seus nomes editoriais resolvidos pela fonte global `teamDisplayName`. A comparação ignora acentos e trata hífens/espaços de forma equivalente. O memorial “Chicão — O Deus da Raça” entra como resultado editorial próprio e aponta para `/site/chicao`; não foi convertido em item do catálogo.

As páginas dos oito registros sem mídia continuam acessíveis e agora informam explicitamente: “Registro histórico preservado sem mídia disponível.” Nenhum registro, imagem ou erro foi ocultado. Nenhum asset foi inventado, copiado ou associado por exceção.

## Diagnóstico individual dos oito registros

| Rota | Stable key / ID da View | Evidência histórica | Classificação | Tratamento ET-026 |
|---|---|---|---|---|
| `/site/items/brasil/teams/atletico/items/1988` | `item:07e6f78f…9024f` / 50372 | `paises/brasil/atletico/1988.htm`; zero referências de imagem; página agregada `unsupported` | `REVIEW_REQUIRED` | Aviso público explícito; sem associação artificial |
| `/site/items/brasil/teams/corinthians/collections/04-09/1985` | `item:903c5ff7…73dd` / 50782 | HTML aponta `2.jpg`, `0.jpg` e `04_09/ne5.jpg`; os três arquivos estão ausentes do Inventory/workspace | `INVALID_READY_STATE` | Aviso público; correção de status exige camada derivada e ficou fora do escopo |
| `/site/items/brasil/teams/selecaob/items/1972-fc0de5` | `item:069ad9af…626e` / 51695 | HTML aponta `pel%E972.jpg`, `pel%E972(1).jpg` e `05_09/pel%E9_72.jpg`; `pelé72.jpg` e `pelé72(1).jpg` existem fisicamente | `RECOVERABLE` | Vínculo não refeito: exige corrigir decodificação e reconstruir camadas protegidas |
| `/site/items/brasil/teams/selecaob/items/2006-8f3c3d` | `item:3dd7f940…0e06` / 51732 | HTML aponta nomes com `%E1`; `kaká2006.jpg`, `kaká06.jpg` e `kaká06(1).jpg` existem fisicamente | `RECOVERABLE` | Vínculo não refeito: exige corrigir decodificação e reconstruir camadas protegidas |
| `/site/items/italia/teams/bologna/items/documento-sem-titulo` | `item:a396513d…32e9` / 51958 | `paises/italia/bologna/untitled.htm`; zero referências; página agregada `unsupported` | `REVIEW_REQUIRED` | Aviso público explícito; sem inferência editorial |
| `/site/items/italia/teams/juventus/items/1944-1945` | `item:4572beec…f25f` / 53186 | `paises/italia/juventus/4445.htm`; zero referências; página agregada `unsupported` | `REVIEW_REQUIRED` | Aviso público explícito; sem inferência editorial |
| `/site/items/italia/teams/sassari/items/1988-1989` | `item:4ba78e1e…960f` / 53802 | HTML aponta `pict0225.jpg` e `pict0226.jpg`; ambos ausentes | `INVALID_READY_STATE` | Aviso público; correção de status exige camada derivada e ficou fora do escopo |
| `/site/items/italia/teams/ternana/items/2002` | `item:84ce7628…c4a` / 53812 | HTML aponta `pict0179.jpg` e `pict0180.jpg`; ambos ausentes | `INVALID_READY_STATE` | Aviso público; correção de status exige camada derivada e ficou fora do escopo |

Os dois casos `RECOVERABLE` não foram corrigidos por tabela paralela no frontend: isso duplicaria a autoridade de associação da Media Layer e contrariaria a proibição de rebuild desta etapa. Os três `INVALID_READY_STATE` também não tiveram o banco alterado. A interface apenas passou a representar honestamente o estado recebido.

## Busca pública

- `Atlético-MG` e `Atletico-MG` encontram a equipe `brasil/atletico`.
- `América` encontra todas as equipes editoriais correspondentes, sem escolher uma arbitrariamente.
- `Grêmio` e `Gremio` encontram `brasil/gremio`.
- `São Paulo` e `Sao Paulo` incluem a entidade equipe `brasil/saopaulo`, preservando resultados de itens da API.
- `Chicão` e `Chicao` incluem a homenagem editorial `/site/chicao`.
- Resultados de equipe devolvidos pela API são deduplicados contra os resultados editoriais.

## Integridade e contagens

Nenhuma camada de Inventory, Parser HTML, Catalog Builder, Normalization, View Model, Media Layer ou Historical Collections foi executada ou alterada. Nenhum banco, workspace, asset protegido, resolver de display, logo ou hero foi modificado.

O banco atual apresentou 3 países, 175 equipes, 930 coleções, 4.465 itens e 16.417 relações de mídia antes e depois. A consulta direta ao último View Run apresentou **351 coleções com `items_count = 0`**, divergindo das 352 documentadas na ET-025. A ET-026 não causou nem corrigiu essa divergência; o valor permaneceu 351 antes/depois e sua investigação continua adiada para a ET-027.

## Validação

- Frontend lint: aprovado.
- Testes existentes de nomes de equipes/países: 6/6 aprovados.
- Testes focados da busca pública: 5/5 aprovados.
- Build de produção: aprovado.
- Backend: 112/112 testes aprovados (uma advertência de depreciação do Starlette).
- Serviços: API `:8000` e frontend `:5173` responderam HTTP 200.
- Oito endpoints de detalhe dos registros sem mídia: HTTP 200.
- Validação visual final pendente para aprovação manual do usuário, pois nenhum navegador estava conectado à sessão.

Nenhum commit e nenhum push foram realizados.
