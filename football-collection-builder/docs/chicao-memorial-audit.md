# Chicão Memorial Audit

## Resumo executivo

Auditoria somente leitura realizada em 19/08/2026, sem consulta externa e sem reconstrução de camadas. A homenagem original foi determinada com evidência direta no workspace histórico configurado no banco: `C:\Users\camilo.tozzi\Desktop\Área de Trabalho\FC\Football Collection`.

O núcleo é composto por três páginas (`chicao/chicao.htm`, `chicao/camisas.htm` e `chicao/videos.htm`), 17 imagens no diretório `chicao`, 3 vídeos AVI e 9 imagens externas explicitamente usadas pela página de camisas. A entrada original aparece nas páginas iniciais em português, italiano e inglês. A página principal tem o título **“CHICÃO - \"O DEUS DA RAÇA\"”**, quatro imagens ligadas a clubes/seleção, um depoimento assinado por Mauro Matta e links para Camisas e Vídeos.

Foram encontradas 70 linhas textuais relevantes na árvore histórica principal incluindo a cópia publicada em `public/`, distribuídas entre a homenagem, seus links de entrada e registros de camisas que mencionam Chicão. A busca no repositório novo encontrou somente um fixture de teste genérico com `CHICAO`; não existe rota, componente ou conteúdo memorial no frontend público atual.

Situação resumida das imagens potencialmente relacionadas: **26 confirmadas**, **3 prováveis** e **3 indeterminadas**. A identidade de pessoas nas imagens não foi inferida visualmente; as classes decorrem exclusivamente de paths, HTML, legendas e nomes.

## Evidências encontradas

### Fontes principais

| Fonte | Evidência | Papel |
|---|---|---|
| `chicao/chicao.htm` | título, depoimento, 6 imagens e links internos | página memorial principal |
| `chicao/camisas.htm` | 16 referências de imagem em 7 blocos editoriais | acervo de camisas relacionado |
| `chicao/videos.htm` | 3 embeds antigos do YouTube e respectivas legendas | acervo audiovisual |
| `paises.htm` | imagem `chicao/0001.jpg` e link memorial em português, italiano e inglês | entrada principal |
| `paises_ita.htm` | imagem clicável e texto em italiano | entrada alternativa |
| `paises_ing.htm` | imagem clicável e texto em inglês | entrada alternativa |
| `paises/**` | legendas de itens de São Paulo, Seleção, Atlético, Corinthians e Flamengo | referências editoriais paralelas; nem todas pertencem ao memorial |
| `inventario-footballcollection.csv` em `.pull-staging` | 21 registros sob `chicao/` na versão ali inventariada | evidência de inventário anterior |
| banco atual | 23 itens sob `chicao/`: 17 imagens, 3 páginas e 3 vídeos | preservação no Inventory atual |

### Contagem e escopo

- 70 linhas com ocorrência textual/path relevante na árvore histórica principal, contando os duplicados publicados em `public/`.
- 31 paths cujo nome ou diretório contém `chicao` fora de `public`, `dist`, `node_modules` e `.git`: 23 itens do núcleo, 8 imagens de camisas com nome contendo `chicao`.
- 3 páginas memoriais parseadas no run HTML atual.
- 5 links internos resolvidos entre as 3 páginas: principal → Camisas; principal → Vídeos; principal → `paises.htm`; Camisas → principal; Vídeos → principal.
- 3 cópias históricas adicionais examinadas em `C:\Projetos\Football Collection*`. Os binários do núcleo têm hashes coincidentes entre as cópias; os HTMLs modernizados diferem do original e perdem conteúdo editorial, portanto o workspace configurado no banco é a fonte mais completa.

## Página/homenagem original

**Página:** `chicao/chicao.htm`  
**Título HTML:** `Chicão - O Deus da Raça`  
**Título visível:** `CHICÃO - "O DEUS DA RAÇA"`  
**Idioma/encoding:** HTML em português, `iso-8859-1`, entidades HTML.  
**Autoria do depoimento:** Mauro Matta.  
**Data de publicação:** **NÃO DETERMINADO**. Os timestamps históricos dos arquivos vão de setembro a dezembro de 2008, mas não provam a data de publicação.

Estrutura visual original aproximada:

1. fundo azul escuro (`#000099`) e texto branco;
2. título centralizado;
3. composição em tabela de três colunas;
4. imagens “SÃO PAULO”, “SELEÇÃO BRASILEIRA”, “SANTOS” e “ATLÉTICO MINEIRO” ao redor de um quadro central;
5. depoimento no quadro central inferior;
6. botões visuais “CAMISAS” e “VÍDEOS” abaixo;
7. link “VOLTAR” para `../paises.htm`.

Não há subtítulo separado além de “O Deus da Raça”. Não foram encontradas legendas nominais das fotografias nem datas pessoais na página principal.

## Textos históricos

O depoimento original, preservado em `chicao/chicao.htm`, é:

> Sem dúvida foi um Amigo em pouco tempo, um rapaz simples, um Homem seguro em campo e ao mesmo tempo, um menino humilde fora dele, valorizava a minha pessoa mais do que devia, para ele talvez a nossa amizade era bem mais do que uma simples Amizade, me fez sentir um irmão e me tratou as vezes como filho.
>
> Posso afirmar que tenho muito orgulho em ter conhecido este menino maravilhoso com um coração enorme, este homem humilde e carinhoso com todas as pessoas que tiveram oportunidade de conhecê-lo.
>
> Lembro me como se fosse hoje a primeira vez em que o conheci em 1988, fiquei muito impressionado quanto a bondade e humildade dele, e sem dúvida, foi com esta mesma humildade e bondade, que ele se apresentou a DEUS.
>
> Mauro Matta

Textos de entrada encontrados:

- português: “Link inteiramente dedicado à memória de meu grande amigo Chicão.”
- italiano: “Link dedicato alla memoria del mio grande amico Chicão.”
- inglês: “Link dedicated to the memory of my great friend Chicão.”

Blocos da página `chicao/camisas.htm`, preservados sem modernização editorial:

- `CHICÃO - SÃO PAULO CAMPEONATO BRASILEIRO 1977 - ORIGINAL`
- `CAMISA RETRÔ REEBOK - CHICÃO - ORIGINAL`
- `HOMENAGEM DO SÃO PAULO F.C. - ORIGINAL JOGO: SÃO PAULO 2 x 1 VITÓRIA - 23/10/2008`
- `COPA DO MUNDO DA ARGENTINA 1978 CHICÃO - ARGENTINA x BRASIL - ORIGINAL`
- `CHICÃO - SELEÇÃO MASTER 1991 - ORIGINAL`
- `CHICÃO - ATLÉTICO MINEIRO CAMPEONATO BRASILEIRO 1979 - ORIGINAL`
- `CHICÃO - ATLÉTICO MINEIRO CAMPEONATO BRASILEIRO 1980 - ORIGINAL`

Textos de `chicao/videos.htm`: `FINAL BRASILEIRO 1977`, `CHICÃO PERDE O BIGODE` e `ENTREVISTA EM 2005`.

## Imagens e mídia

### Imagens confirmadas

As 26 imagens abaixo são confirmadas porque estão no diretório documental `chicao/` ou são referenciadas diretamente por `chicao/chicao.htm`/`chicao/camisas.htm`. “Refs.” conta referências dentro do núcleo memorial, não duplicações em outras páginas. Nenhuma das 17 imagens do diretório memorial possui media key no Media Layer atual.

| Path relativo | Dimensões | Bytes | SHA-256 | Refs. | Estado atual |
|---|---:|---:|---|---:|---|
| `chicao/0001.jpg` | 118×252 | 20.382 | `93095b975365d2ac8521bd9bbe8d172430de6fe1a94ab96f7d6794c65ef7b8a7` | 1+ entradas | Inventory; Parser `referenced`; fora da Media Layer |
| `chicao/atletico.jpg` | 200×300 | 27.728 | `7f636f2b52b3352d413aef7e18d089a6066813bba6c2972307b2e266847ed60c` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/brasil.jpg` | 200×300 | 31.231 | `328e95c9742553ca9380408451f31df3bbd084aff242c0c1182f90dfe2575faa` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/brasilshirt.jpg` | 182×225 | 20.326 | `af1a12e4a3cfcabed65880e51c9812ea9515594c2c8331a4095747c411ff5651` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/camisas/homenagem.jpg` | 500×323 | 76.298 | `8a4e74bdeb4205f5932795c612ea87a40a3587933d098a83a38324b6bfaacc8c` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/camisas/jhg_002.jpg` | 250×292 | 29.431 | `e289f91fbe13c4c747e142af73ad0e2319a9f0747349c2270c578df5df76073c` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/camisas/jhg_003.jpg` | 250×292 | 33.199 | `2e0098d26f7ec7d5d3c2a78a3f78a667a7643ff87ce5e8697c222caf2b020669` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/camisas/jhg_005.jpg` | 250×292 | 23.019 | `f267ead5ce248d5e2ba4aed0236857eb4f4147ecb15ab50a7467279773128f72` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/camisas/jhg_008.jpg` | 250×292 | 23.463 | `74d01b67d5526b70b84c45e44aca4cce17fb3407edef9610058db49efacafeb2` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/camisas/xcv_003.jpg` | 250×292 | 30.169 | `e5c04ca2894cd32e4c824e6307e93cbb6fb074129a15c307cfcc57d4adcb6283` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/camisas/xcv_006.jpg` | 250×292 | 29.406 | `fdb909b4771ea0522a2e03dde891198b45eff8f7b69fc8a7b8e65db7032eda6a` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/depoimentos.jpg` | 937×430 | 75.211 | `e6899bbf72bd8c7ba037b24b6b0871832e9b953184171e43f2315dc3222c4e23` | 0 | Inventory; Parser `orphan`; fora da Media Layer |
| `chicao/depoimentos2.jpg` | 150×69 | 17.947 | `291efbd34c44fac47f117df533cf2b1cf2776ecd8257db530b1c70fae8b94651` | 0 | Inventory; Parser `orphan`; fora da Media Layer |
| `chicao/santos.jpg` | 200×300 | 27.131 | `5df96636a3b4403bfe8f8ef8c55d61a197bdb4088175fed472a5a47c9988fa33` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/sao paulo.jpg` | 200×300 | 35.218 | `5b59bf24b974b3f95927d560f3f59321910807cff1b713bcf2c0f0bb8bb6c349` | 1 | Inventory; referenced; fora da Media Layer |
| `chicao/trofeu 77.bmp` | 66×160 | 42.294 | `a21b48620477984c67d7f5b124a9ffa4a837783f47b33b6a51a4442e5275c7d7` | 0 | Inventory; Parser `orphan`; fora da Media Layer |
| `chicao/videos2.jpg` | 171×225 | 35.615 | `2952382d5d2b494cd84dba23fc7077b450f930c13cfffce10b9c01523cc7a256` | 1 | Inventory; referenced; fora da Media Layer |
| `camisas/brasil/saopaulo/3850.JPG` | 250×292 | 23.126 | `a4b4400dbeb16ccb8f2aed7c0580ab51a372091839c12fdfaf008b26810fe01c` | 1 | Inventory/Parser; memorial Camisas |
| `camisas/brasil/saopaulo/3851.JPG` | 250×292 | 21.647 | `4dffe37c578a5a9aa0445a348e797f0c7624c153851e3740374c4e41d682cf3c` | 1 | Inventory/Parser; memorial Camisas |
| `camisas/brasil/selecao/3845.JPG` | 250×292 | 23.388 | `bb82743ed61568fe2b92100ea27b7ff6fa4b88eccfba38c0c75a431d4b99b5df` | 1 | Inventory/Parser; memorial Camisas |
| `camisas/brasil/selecao/3844.JPG` | 250×292 | 26.087 | `c219026c7db18c76dedc835ea2baaf4fc71919c082084e4aec46b811f3d1604c` | 1 | Inventory/Parser; memorial Camisas |
| `camisas/brasil/selecao/0001.jpg` | 118×292 | 18.938 | `6a4093cc0e90c4bb94a258e0243ec3a012b231ee3f6d7de16b65d6b706d8a021` | 1 | Inventory/Parser; memorial Camisas |
| `camisas/brasil/atletico/coppa012.jpg` | 250×292 | 32.213 | `f00c0d350f53a093da641531ac746c482b93a01071b9c4b986c3508e9bd3c93b` | 1 | Inventory/Parser; memorial Camisas |
| `camisas/brasil/atletico/coppa013.jpg` | 250×292 | 34.331 | `68f4222e1321c73a5720a714bf9edab6207ad21b00589209d45a516ace5116c4` | 1 | Inventory/Parser; memorial Camisas |
| `camisas/brasil/atletico/atletico_m.g._1980_chicao_camp.brasileiro.jpg` | 250×292 | 30.010 | `59027e89f9c0a9c237f335c80c098b29bf461ec5155f18b68c8edfc77ab6c968` | 1 | Media key `media-5d38f64fbf8a7c6a`; disponível |
| `camisas/brasil/atletico/atletico_m.g._1980_chicao_camp.brasileiro_(1).jpg` | 250×292 | 31.003 | `9a3afbec47647f5c8ff28ff79af13b78f96790e3e41f95f824c4061aeff6ca8b` | 1 | Media key `media-db0b0ac699fa416d`; disponível |

### Prováveis

| Path | Evidência | Motivo da cautela |
|---|---|---|
| `camisas/brasil/atletico/chicao.jpg` | nome e diretório do Atlético, coerentes com o memorial | não referenciada diretamente pelas páginas memoriais encontradas |
| `camisas/brasil/atletico/chicao_1979.jpg` | nome, ano e legenda histórica do Atlético 1979 | não faz parte da página memorial `camisas.htm`; media key `media-ec9cf8a779d5bb49` |
| `camisas/brasil/saopaulo/fot_gio/chicao77.jpg` | nome, ano e legenda São Paulo 1977 | não faz parte da página memorial; media key `media-12a9b14a2f8306c9` |

### Indeterminadas

| Path | Evidência | Motivo |
|---|---|---|
| `camisas/brasil/corinthians/chicao_2012_(1).jpg` | nome/legenda `CHICÃO` | contexto Corinthians 2012, fora do memorial; media key `media-605d7dc6ede527e0` |
| `camisas/brasil/corinthians/chicao_2012_(2).jpg` | nome/legenda `CHICÃO` | contexto Corinthians 2012, fora do memorial; media key `media-494269bc8e58fcc8` |
| `camisas/brasil/corinthians/chicao_2012_(3).jpg` | nome/legenda `CHICÃO` | contexto Corinthians 2012, fora do memorial; media key `media-5a023cd6ca93ca60` |

Há ainda legendas `CHICÃO` em páginas Corinthians 2010 e Flamengo 2014 sem filename inequivocamente relacionado no resultado textual. Elas não devem ser incorporadas ao memorial sem decisão documental.

### Vídeos confirmados

| Path local | Bytes | Evidência |
|---|---:|---|
| `chicao/YOUTUBE/Brasileiro 1977.avi` | 34.266.710 | diretório memorial e legenda `FINAL BRASILEIRO 1977` |
| `chicao/YOUTUBE/Entrevista em 2005.avi` | 10.112.296 | diretório memorial e legenda correspondente |
| `chicao/YOUTUBE/São Paulo 3x2 Santos_ 1981_ Chicão perde o bigode.avi` | 13.678.718 | diretório, filename e legenda correspondentes |

O HTML original também contém embeds Flash dos IDs antigos do YouTube `AmSocBo71-s`, `JTDgw_NV-aU` e `NnQ8LeICb1k`. Disponibilidade externa não foi verificada, conforme proibição de pesquisa na Internet.

## Links e navegação original

Fluxo determinado:

`content.htm` → `paises.htm` / `paises_ita.htm` / `paises_ing.htm` → imagem `chicao/0001.jpg` e/ou texto memorial → `chicao/chicao.htm` → `chicao/camisas.htm` ou `chicao/videos.htm` → voltar à página principal → `paises.htm`.

Detalhes:

- Em `paises.htm`, somente o texto português contém o `<a>` no HTML original; a imagem não é clicável. As frases italiana e inglesa são texto informativo.
- Em `paises_ita.htm` e `paises_ing.htm`, a imagem `0001.jpg` é clicável.
- A página principal oferece somente Camisas, Vídeos e Voltar.
- Camisas e Vídeos retornam a `chicao.htm`.
- Não foi encontrado link memorial em menu global ou footer independente.

## Situação no catálogo atual

| Camada | Situação |
|---|---|
| Inventory | **Preservado**: 23 itens do núcleo `chicao/` (17 imagens, 3 HTMLs, 3 AVIs). |
| Parser HTML | **Preservado**: 3 páginas parseadas; imagens e 5 links internos resolvidos. O texto principal fica truncado a 500 caracteres no `text_preview`, embora o HTML original permaneça no workspace. |
| Image Parser | **Preservado parcialmente**: 17 imagens válidas; 14 referenciadas e 3 órfãs (`depoimentos.jpg`, `depoimentos2.jpg`, `trofeu 77.bmp`). |
| Catalog Builder | **Ignorado estruturalmente**: nenhum item do build 10 com título/path memorial; o Builder deriva entidades sob `paises/`. |
| Quality / Review / Normalization | **Não incorporado**: sem entidade memorial a analisar/normalizar. |
| View Model | **Não transportado**: zero itens memoriais no view run 15. |
| Media Layer | **Não transportado como memorial**: zero assets do diretório `chicao/` no run 17. Sete imagens de camisas com `chicao` no filename aparecem por relações normais do catálogo. |
| Historical Collections | **Fora do escopo atual da camada**: zero itens no run 1; a camada cobre Pennants, Flags e Memorabilia. |
| Rotas públicas | **Inexistentes** para a homenagem. |

Os runs atuais foram somente consultados: Inventory 1, HTML Parser 3, Image Parser 2, Catalog 10, Quality 7, Normalization 9, View Model 15, Media Layer 17 e Historical Collections 1.

## Situação no frontend novo

Classificação: **A) não existe implementação**.

Não há ocorrência de Chicão em componentes, páginas, rotas, configurações, assets, textos, links, placeholders ou TODOs do frontend atual. Também não há conteúdo memorial oculto ou rota preparada. A única ocorrência no código novo é um fixture sintético `CHICAO` em `backend/tests/test_catalog_editorial_records.py`, sem relação funcional com a homenagem.

## Conteúdo preservado

- HTML original integral das três páginas no workspace configurado.
- Depoimento integral e assinatura.
- Títulos, legendas, composição e links originais.
- 17 imagens do diretório memorial e 9 imagens externas usadas por Camisas.
- 3 vídeos AVI locais.
- Entradas em português, italiano e inglês.
- Metadados e referências no Inventory/Parsers.
- Cópias históricas redundantes dos binários.

## Conteúdo atualmente não exposto

- toda a página memorial e seu depoimento;
- as 17 imagens próprias do núcleo;
- a curadoria de 7 blocos de camisas como conjunto memorial;
- os 3 vídeos e suas legendas;
- os textos de entrada multilíngues;
- `depoimentos.jpg`, `depoimentos2.jpg` e `trofeu 77.bmp`, hoje órfãos no Parser;
- qualquer navegação pública dedicada.

## Riscos

- **Identidade ambígua:** registros Corinthians/Flamengo podem se referir a homônimo; não misturar sem evidência.
- **Perda editorial em derivados:** cópias modernizadas de `chicao.htm` removeram o depoimento; usar sempre o HTML original configurado no Inventory como fonte.
- **Paths divergentes:** uma cópia em `C:\Projetos\Football Collection` achata sete arquivos de `chicao/camisas/`, quebrando referências; o workspace configurado e as cópias `_old` preservam a hierarquia correta.
- **Encoding:** o original usa ISO-8859-1 e entidades; conversão descuidada produz mojibake.
- **Vídeos antigos:** embeds Flash/YouTube não são solução moderna e a disponibilidade externa é desconhecida; AVIs exigem estratégia de entrega/transcodificação futura.
- **Privacidade/direitos:** autoria, consentimento, direitos de imagem e de vídeo não estão documentados no workspace.
- **Imagens órfãs:** `depoimentos*` e `trofeu 77.bmp` pertencem ao diretório, mas sua posição editorial original não foi determinada.
- **Baseline protegido:** inserir conteúdo dentro de seções atuais arriscaria regressões nas ET-020–ET-023A.

## Possíveis formas de integração futura

| Alternativa | Vantagens | Riscos/impacto |
|---|---|---|
| Página memorial própria | preserva texto, mídia e contexto; rota isolada; baixo risco ao layout atual | exige contrato de dados/mídia e decisão de URL |
| Seção independente na Home | restaura visibilidade histórica e acesso direto | aumenta comprimento da Home e pode competir com seções aprovadas |
| Link editorial no footer | impacto visual mínimo e navegação estável | homenagem fica pouco visível |
| Home + página própria | melhor equilíbrio entre descoberta e profundidade | requer dois pontos de integração e arte/resumo aprovados |
| Entrada em área editorial independente | separa memorial de catálogo e coleções | exige definir nova taxonomia pública |

Nenhuma alternativa foi escolhida nesta auditoria. Hero, estatísticas, Explore o acervo, Países e regiões, Equipes em destaque, Coleções, Coleções Históricas, cards, artes, escudos ET-022R, resolvers ET-023/023A, slugs, rotas e assets atuais podem permanecer intactos em todas as opções acima.

## Recomendações técnica preliminar

A opção preliminar de menor acoplamento é **página memorial própria, com uma chamada pequena e independente na Home ou no footer**, sem reutilizar nem substituir seções existentes. O conteúdo deve vir de um modelo editorial dedicado, não do Catalog Builder de camisas nem de Historical Collections.

Antes de implementar:

1. congelar uma cópia lógica dos 3 HTMLs, 26 imagens confirmadas e 3 AVIs por hash;
2. preservar o depoimento literalmente, submetendo qualquer correção ortográfica a aprovação explícita;
3. excluir inicialmente os 3 itens Corinthians indeterminados;
4. decidir se os 3 itens prováveis entram no memorial;
5. definir tratamento dos 3 visuais órfãos;
6. definir política de vídeo e direitos;
7. criar contrato de Media Layer específico sem reconstruir ou alterar os runs históricos existentes.

## Itens que exigem decisão do usuário

- URL e nome público da futura página.
- Página própria, Home, footer ou combinação.
- Preservação literal ou revisão aprovada de capitalização/pontuação do depoimento.
- Uso de `depoimentos.jpg`, `depoimentos2.jpg` e `trofeu 77.bmp` e sua ordem.
- Inclusão dos 3 itens prováveis.
- Exclusão/confirmação documental dos 3 itens Corinthians e das legendas Corinthians/Flamengo.
- Quais imagens devem ser capa, galeria e thumbnails.
- Uso dos AVIs locais, conversão futura ou links externos.
- Créditos, direitos e eventual aviso memorial.
- Necessidade de manter os textos italiano e inglês.

## Integridade da auditoria

- Operação executada em modo somente leitura sobre workspace histórico, banco e código.
- Nenhum build de Inventory, Parser, Catalog, Quality, Review, Normalization, View Model, Media Layer ou Historical Collections foi disparado.
- Banco SQLite foi aberto com `mode=ro`; os runs existentes foram preservados.
- Nenhum HTML, imagem, vídeo, timestamp, frontend, backend, catálogo ou banco foi alterado.
- Nenhum README, changelog ou roadmap foi alterado.
- O único arquivo criado foi `docs/chicao-memorial-audit.md`.
- Nenhum commit ou push foi realizado.

