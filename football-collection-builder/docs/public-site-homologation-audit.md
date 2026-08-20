# ET-025 ? Homologa??o completa do site p?blico ? auditoria read-only

_Executada em 2026-08-20T13:57:30Z; crawler integral local em 512.14s._

## Resumo executivo

| Indicador | Resultado |
|---|---:|
| Total de URLs/alvos testados | **30.010** |
| Rotas visuais e links internos deduplicados | **7137** |
| Endpoints sem?nticos de entidades | **7269** |
| M?dias p?blicas ?nicas do cat?logo | **15587** |
| Assets est?ticos cr?ticos | **10** |
| Consultas de busca | **7** |
| Rotas PASS | **6758** |
| Rotas WARNING | **371** |
| Rotas FAIL | **8** |
| Pa?ses/regi?es | **3** |
| Equipes | **175** |
| Cole??es | **930** |
| Temporadas derivadas | **1.500** |
| Itens do cat?logo | **4.465** |
| Itens de cole??es hist?ricas | **196** |
| Rela??es de m?dia declaradas no summary | **16.417** |
| Refer?ncias de m?dia observadas nos payloads auditados | **51.340** |
| M?dias ?nicas testadas (incluindo 10 est?ticas) | **15.597** |

Todos os 7.137 caminhos visuais responderam HTTP 200. A classifica??o WARNING/FAIL incorpora consist?ncia sem?ntica; portanto, n?o equivale apenas ao status HTTP. Todos os 7.269 endpoints de entidade responderam corretamente. As 15.587 m?dias do cat?logo responderam HTTP 206 com MIME v?lido: 15.325 JPEG, 170 GIF e 92 PNG.

## Escopo e m?todo

- Enumera??o paginada integral pelas APIs p?blicas atuais; nenhuma amostragem.
- Valida??o dupla: rota SPA e endpoint sem?ntico de pa?s, equipe, cole??o, temporada, item ou cole??o hist?rica.
- M?dias deduplicadas por URL e testadas com requisi??o Range de um byte.
- Associa??es pa?s/equipe/cole??o e rotas duplicadas verificadas em todos os itens.
- Nenhum endpoint de build, persist?ncia ou muta??o foi chamado.
- O relat?rio ? o ?nico arquivo funcional criado pela ET-025. O build produziu somente artefatos transit?rios em `frontend/dist`.

## Resultado por dom?nio

### Pa?ses e regi?es

| Slug | Display | Equipes | Cole??es | Itens | Branding | HTTP | Status |
|---|---|---:|---:|---:|---|---:|---|
| brasil | Brasil | 49 | 381 | 1565 | sim | 200 | PASS |
| italia | It?lia | 59 | 479 | 2666 | sim | 200 | PASS |
| outros | Outros | 67 | 70 | 234 | sim | 200 | WARNING |

N?o foram encontradas associa??es de equipe com pa?s incorreto. Os slugs permaneceram `brasil`, `italia` e `outros`.

### Cole??es e temporadas

- 930/930 endpoints de cole??o e 1.500/1.500 endpoints de temporada responderam corretamente.
- Nenhuma temporada estava vazia.
- 352 cole??es possuem zero itens e foram classificadas como WARNING.
- Uma cole??o (`italia/torino/outros`) permanece `review_required`.

### Itens

- 4.465/4.465 endpoints sem?nticos e rotas visuais responderam.
- Nenhuma rota de item duplicada e nenhuma associa??o pa?s/equipe divergente.
- Oito itens `ready` n?o possuem m?dia e s?o FAIL; est?o no Ap?ndice C.
- Um item Torino `outros-82b271` permanece `review_required`.

### M?dias

- 15.587 URLs ?nicas do cat?logo: 100% HTTP 206, Range funcional e MIME de imagem coerente.
- 10 assets cr?ticos est?ticos: 7 imagens e 3 MP4, todos HTTP 206 e MIME correto.
- Nenhuma URL quebrada foi encontrada.

### Busca

| Termo | Total API | Avalia??o |
|---|---:|---|
| S?o Paulo | 5 | WARNING: apenas itens; equipe n?o retornada |
| Atl?tico-MG | 0 | FAIL |
| Am?rica-MG | 0 | FAIL |
| Gr?mio | 0 | FAIL |
| Juventus | 3 | PASS: equipe + 2 itens |
| Chic?o | 0 | WARNING: memorial n?o pesquis?vel |
| termo-inexistente-et025 | 0 | PASS |

### Home, navega??o e memorial Chic?o

- Home, menu, busca, seis entradas principais e memorial responderam HTTP 200.
- As tr?s p?ginas de camisa usam `PublicEditorialRecord`; Santos permanece sem link.
- Depoimento e cr?dito Mauro Matta continuam presentes no c?digo atual.
- Tr?s MP4 responderam Range/206 com `video/mp4`; hashes e metadados coincidem com ET-024D.
- AVI originais foram apenas lidos para hash e mant?m os hashes documentados.

### V?deos

| Arquivo | Bytes | Codec/resolu??o/fps | Dura??o | SHA-256 |
|---|---:|---|---:|---|
| brasileiro-1977.mp4 | 21.585.868 | H.264 320?256 30 fps; AAC mono | 207,020s | `3678E2DC?27FE40A2` |
| entrevista-2005.mp4 | 4.143.094 | H.264 320?240 25 fps; AAC mono | 239,046s | `A56F5064?1F3A8EB` |
| sao-paulo-3x2-santos-1981-chicao-perde-o-bigode.mp4 | 9.356.092 | H.264 320?198 15 fps; AAC mono | 200,490s | `D183C9CC?A5EDF1CD` |

## Testes t?cnicos

- `npm run lint`: PASS.
- Testes frontend team/country: 6/6 PASS; dois avisos experimentais do Node sobre Type Stripping.
- `npm run build`: PASS; 137 m?dulos; aviso/falha zero.
- Pytest backend: 112/112 PASS; 1 `StarletteDeprecationWarning` preexistente.

## Tabela consolidada de problemas

| ID | Severidade | Categoria | Entidade | Rota/Asset | Problema | Evid?ncia | A??o sugerida |
|---|---|---|---|---|---|---|---|
| ET025-001 | HIGH | Itens | 8 itens ready | 8 rotas | Itens publicados sem m?dia principal ou adicional. | API detail: media=[] e imagesCount=0. | Revisar origem/normaliza??o em ET pr?pria; n?o publicar como ready sem m?dia. |
| ET025-002 | MEDIUM | Cole??es | 352 cole??es | Ap?ndice B | Cole??es p?blicas respondem, mas possuem zero itens. | items.total=0 em 352/930 detalhes. | Decidir se devem ser ocultadas, consolidadas ou preenchidas. |
| ET025-003 | HIGH | Busca | Nomes aprovados | /site/busca | Atl?tico-MG, Am?rica-MG e Gr?mio retornam zero resultados. | Busca usa nomes persistidos e n?o os display names resolvidos no frontend. | Integrar aliases de display ao ?ndice/consulta sem alterar slugs. |
| ET025-004 | MEDIUM | Busca | S?o Paulo | /site/busca | Retorna cinco itens, mas n?o a entidade equipe S?o Paulo. | Equipe persistida como saopaulo n?o casa com o termo exibido. | Auditar busca por aliases de equipes. |
| ET025-005 | MEDIUM | Busca | Chic?o | /site/busca | A busca global retorna zero para a homenagem p?blica. | Memorial n?o integra o cat?logo pesquis?vel. | Decidir inclus?o editorial da rota memorial na busca. |
| ET025-006 | REVIEW | Team Branding | 6 equipes | Ap?ndice A | Seis equipes n?o possuem logo; fallback textual funciona. | logoMedia ausente; rotas e conte?do v?lidos. | Validar humanamente se aus?ncia ? esperada. |
| ET025-007 | REVIEW | Nomes | 6 equipes amb?guas | Ap?ndice A | Casos hist?ricos permanecem amb?guos conforme ET-023. | jrcasale, borussia, dinamo, rosario, sanjose e sparta. | Manter sem normaliza??o autom?tica at? evid?ncia. |
| ET025-008 | REVIEW | Status editorial | Entidades review_required | Cat?logo p?blico | 1 pa?s, 1 cole??o, 1 item e 3 itens hist?ricos continuam em revis?o. | publicStatus/status persistido como review_required. | Revis?o humana antes da V1.0. |
| ET025-009 | LOW | Git | Reposit?rio | C:\ | A raiz Git detectada abrange o disco inteiro; status completo expirou. | git rev-parse retornou C:/ e git status percorreu diret?rios do sistema. | Corrigir/limitar a raiz Git em tarefa de infraestrutura separada. |
| ET025-010 | REVIEW | Visual/console | Site completo | Todas as rotas | Browser integrado indispon?vel; responsividade e console n?o foram observados. | Auditoria HTTP/API completa, sem sess?o visual integrada. | Validar manualmente 1920/1440/1024/768/390/360 e console. |

### Totais por severidade

- CRITICAL: **0**
- HIGH: **2**
- MEDIUM: **3**
- LOW: **1**
- REVIEW: **4**

## Prioriza??o

### Bloqueadores para produ??o
- Nenhum CRITICAL t?cnico de disponibilidade foi encontrado.

### Corrigir antes da V1.0
- ET025-001: oito itens `ready` sem m?dia.
- ET025-003: busca n?o reconhece tr?s display names aprovados.
- ET025-002: decidir tratamento das 352 cole??es vazias.
- ET025-004/005: cobertura de S?o Paulo e Chic?o na busca.

### Pode ser corrigido depois da V1.0
- ET025-009: delimita??o da raiz Git, desde que o fluxo atual permane?a controlado.

### Valida??o humana necess?ria
- ET025-006, ET025-007, ET025-008 e ET025-010.

## Limita??es

- Browser integrado indispon?vel: `VISUAL_REVIEW_REQUIRED` em 1920, 1440, 1024, 768, 390 e 360 px; console JavaScript e layout n?o puderam ser observados.
- A raiz Git detectada ? `C:/`; `git status` percorreu o disco do sistema e expirou. N?o foi poss?vel obter snapshot Git confi?vel antes/depois. Nenhum arquivo foi limpo ou revertido.
- HTTP 200 das rotas SPA foi sempre combinado com valida??o da API para evitar aprova??o baseada no fallback do Vite.

## Ap?ndice A ? 175 equipes

| Pa?s | Slug | Nome persistido | Display Name | Rota | Logo | Cole??es | Itens | HTTP | Status | Observa??o |
|---|---|---|---|---|---|---:|---:|---:|---|---|
| brasil | `america-mg` | america_mg | América-MG | `/site/paises/brasil/equipes/america-mg` | yes | 2 | 5 | 200 | PASS | ? |
| brasil | `america-rj` | america_rj | América-RJ | `/site/paises/brasil/equipes/america-rj` | yes | 2 | 3 | 200 | PASS | ? |
| brasil | `america-rn` | america rn | América-RN | `/site/paises/brasil/equipes/america-rn` | yes | 0 | 3 | 200 | PASS | ? |
| brasil | `anapolina` | anapolina | Anapolina | `/site/paises/brasil/equipes/anapolina` | yes | 0 | 2 | 200 | PASS | ? |
| brasil | `atletico` | atletico | Atlético-MG | `/site/paises/brasil/equipes/atletico` | yes | 60 | 368 | 200 | PASS | ? |
| brasil | `atleticop` | atleticop | Atlético-PR | `/site/paises/brasil/equipes/atleticop` | yes | 5 | 9 | 200 | PASS | ? |
| brasil | `bahia` | bahia | Bahia | `/site/paises/brasil/equipes/bahia` | yes | 11 | 10 | 200 | PASS | ? |
| brasil | `botafogo` | botafogo | Botafogo | `/site/paises/brasil/equipes/botafogo` | yes | 13 | 43 | 200 | PASS | ? |
| brasil | `botafogo-sp` | botafogo_sp | Botafogo-SP | `/site/paises/brasil/equipes/botafogo-sp` | yes | 0 | 2 | 200 | PASS | ? |
| brasil | `capivariano` | capivariano | Capivariano | `/site/paises/brasil/equipes/capivariano` | yes | 2 | 4 | 200 | PASS | ? |
| brasil | `caxias` | caxias | Caxias | `/site/paises/brasil/equipes/caxias` | yes | 1 | 2 | 200 | PASS | ? |
| brasil | `ceara` | ceara | Ceará | `/site/paises/brasil/equipes/ceara` | yes | 2 | 6 | 200 | PASS | ? |
| brasil | `chapecoense` | chapecoense | Chapecoense | `/site/paises/brasil/equipes/chapecoense` | yes | 6 | 8 | 200 | PASS | ? |
| brasil | `corinthians` | corinthians | Corinthians | `/site/paises/brasil/equipes/corinthians` | yes | 36 | 148 | 200 | PASS | ? |
| brasil | `coritiba` | coritiba | Coritiba | `/site/paises/brasil/equipes/coritiba` | yes | 0 | 3 | 200 | PASS | ? |
| brasil | `cruzeiro` | cruzeiro | Cruzeiro | `/site/paises/brasil/equipes/cruzeiro` | yes | 24 | 85 | 200 | PASS | ? |
| brasil | `csa` | csa | CSA | `/site/paises/brasil/equipes/csa` | yes | 2 | 2 | 200 | PASS | ? |
| brasil | `etti` | etti | Etti Jundiaí | `/site/paises/brasil/equipes/etti` | yes | 0 | 4 | 200 | PASS | ? |
| brasil | `flamengo` | flamengo | Flamengo | `/site/paises/brasil/equipes/flamengo` | yes | 18 | 80 | 200 | PASS | ? |
| brasil | `fluminense` | fluminense | Fluminense | `/site/paises/brasil/equipes/fluminense` | yes | 17 | 35 | 200 | PASS | ? |
| brasil | `fortaleza` | fortaleza | Fortaleza | `/site/paises/brasil/equipes/fortaleza` | yes | 0 | 2 | 200 | PASS | ? |
| brasil | `goias` | goias | Goiás | `/site/paises/brasil/equipes/goias` | yes | 2 | 3 | 200 | PASS | ? |
| brasil | `gremio` | gremio | Grêmio | `/site/paises/brasil/equipes/gremio` | yes | 28 | 102 | 200 | PASS | ? |
| brasil | `guarani` | guarani | Guarani | `/site/paises/brasil/equipes/guarani` | yes | 2 | 17 | 200 | PASS | ? |
| brasil | `internaciol-limeira` | internaciol limeira | Internacional de Limeira | `/site/paises/brasil/equipes/internaciol-limeira` | no | 0 | 4 | 200 | WARNING | sem logo; fallback textual funcional |
| brasil | `internacional` | internacional | Internacional | `/site/paises/brasil/equipes/internacional` | yes | 19 | 42 | 200 | PASS | ? |
| brasil | `ituano` | ituano | Ituano | `/site/paises/brasil/equipes/ituano` | yes | 1 | 2 | 200 | PASS | ? |
| brasil | `juventude` | juventude | Juventude | `/site/paises/brasil/equipes/juventude` | yes | 0 | 2 | 200 | PASS | ? |
| brasil | `londrina` | londrina | Londrina | `/site/paises/brasil/equipes/londrina` | yes | 2 | 3 | 200 | PASS | ? |
| brasil | `marilia` | marilia | Marília | `/site/paises/brasil/equipes/marilia` | yes | 0 | 2 | 200 | PASS | ? |
| brasil | `mirassol` | mirassol | Mirassol | `/site/paises/brasil/equipes/mirassol` | yes | 1 | 3 | 200 | PASS | ? |
| brasil | `noroeste` | noroeste | Noroeste | `/site/paises/brasil/equipes/noroeste` | yes | 1 | 3 | 200 | PASS | ? |
| brasil | `novohorizontino` | novohorizontino | Novorizontino | `/site/paises/brasil/equipes/novohorizontino` | yes | 1 | 2 | 200 | PASS | ? |
| brasil | `palmeiras` | palmeiras | Palmeiras | `/site/paises/brasil/equipes/palmeiras` | yes | 36 | 96 | 200 | PASS | ? |
| brasil | `parana` | parana | Paraná | `/site/paises/brasil/equipes/parana` | yes | 0 | 3 | 200 | PASS | ? |
| brasil | `pontepreta` | pontepreta | Ponte Preta | `/site/paises/brasil/equipes/pontepreta` | yes | 0 | 7 | 200 | PASS | ? |
| brasil | `remo` | remo | Remo | `/site/paises/brasil/equipes/remo` | yes | 0 | 2 | 200 | PASS | ? |
| brasil | `rio-claro` | rio claro | Rio Claro | `/site/paises/brasil/equipes/rio-claro` | yes | 1 | 3 | 200 | PASS | ? |
| brasil | `rio-verde` | rio verde | Rio Verde | `/site/paises/brasil/equipes/rio-verde` | yes | 1 | 2 | 200 | PASS | ? |
| brasil | `santos` | santos | Santos | `/site/paises/brasil/equipes/santos` | yes | 41 | 162 | 200 | PASS | ? |
| brasil | `saocaetano` | saocaetano | São Caetano | `/site/paises/brasil/equipes/saocaetano` | yes | 0 | 8 | 200 | PASS | ? |
| brasil | `saopaulo` | saopaulo | São Paulo | `/site/paises/brasil/equipes/saopaulo` | yes | 24 | 75 | 200 | PASS | ? |
| brasil | `selecaob` | selecaob | Seleção Brasileira | `/site/paises/brasil/equipes/selecaob` | yes | 0 | 115 | 200 | PASS | ? |
| brasil | `selpaulista` | selpaulista | Seleção Paulista | `/site/paises/brasil/equipes/selpaulista` | yes | 0 | 2 | 200 | PASS | ? |
| brasil | `sport` | sport | Sport | `/site/paises/brasil/equipes/sport` | yes | 5 | 10 | 200 | PASS | ? |
| brasil | `taquaritinga` | taquaritinga | Taquaritinga | `/site/paises/brasil/equipes/taquaritinga` | yes | 0 | 2 | 200 | PASS | ? |
| brasil | `vasco` | vasco | Vasco da Gama | `/site/paises/brasil/equipes/vasco` | yes | 9 | 27 | 200 | PASS | ? |
| brasil | `vitoria` | vitoria | Vitória | `/site/paises/brasil/equipes/vitoria` | yes | 1 | 4 | 200 | PASS | ? |
| brasil | `xvpira` | xvpira | XV de Piracicaba | `/site/paises/brasil/equipes/xvpira` | yes | 5 | 38 | 200 | PASS | ? |
| italia | `alessandria` | alessandria | Alessandria | `/site/paises/italia/equipes/alessandria` | yes | 6 | 10 | 200 | PASS | ? |
| italia | `alzano-virescit` | alzano virescit | Alzano Virescit | `/site/paises/italia/equipes/alzano-virescit` | no | 0 | 3 | 200 | WARNING | sem logo; fallback textual funcional |
| italia | `ancona` | ancona | Ancona | `/site/paises/italia/equipes/ancona` | yes | 2 | 6 | 200 | PASS | ? |
| italia | `ascoli` | ascoli | Ascoli | `/site/paises/italia/equipes/ascoli` | yes | 1 | 4 | 200 | PASS | ? |
| italia | `atalanta` | atalanta | Atalanta | `/site/paises/italia/equipes/atalanta` | yes | 4 | 19 | 200 | PASS | ? |
| italia | `avellino` | avellino | Avellino | `/site/paises/italia/equipes/avellino` | yes | 1 | 3 | 200 | PASS | ? |
| italia | `bari` | bari | Bari | `/site/paises/italia/equipes/bari` | yes | 1 | 9 | 200 | PASS | ? |
| italia | `bologna` | bologna | Bologna | `/site/paises/italia/equipes/bologna` | yes | 11 | 29 | 200 | PASS | ? |
| italia | `brescia` | brescia | Brescia | `/site/paises/italia/equipes/brescia` | yes | 2 | 11 | 200 | PASS | ? |
| italia | `cagliari` | cagliari | Cagliari | `/site/paises/italia/equipes/cagliari` | yes | 40 | 318 | 200 | PASS | ? |
| italia | `castel` | castel | Castel di Sangro | `/site/paises/italia/equipes/castel` | yes | 1 | 2 | 200 | PASS | ? |
| italia | `chievo` | chievo | Chievo Verona | `/site/paises/italia/equipes/chievo` | yes | 15 | 41 | 200 | PASS | ? |
| italia | `como` | como | Como | `/site/paises/italia/equipes/como` | yes | 0 | 2 | 200 | PASS | ? |
| italia | `cremonese` | cremonese | Cremonese | `/site/paises/italia/equipes/cremonese` | yes | 1 | 5 | 200 | PASS | ? |
| italia | `crotone` | crotone | Crotone | `/site/paises/italia/equipes/crotone` | yes | 1 | 2 | 200 | PASS | ? |
| italia | `empoli` | empoli | Empoli | `/site/paises/italia/equipes/empoli` | yes | 0 | 2 | 200 | PASS | ? |
| italia | `fiorentina` | fiorentina | Fiorentina | `/site/paises/italia/equipes/fiorentina` | yes | 30 | 153 | 200 | PASS | ? |
| italia | `foggia` | foggia | Foggia | `/site/paises/italia/equipes/foggia` | yes | 2 | 5 | 200 | PASS | ? |
| italia | `genoa` | genoa | Genoa | `/site/paises/italia/equipes/genoa` | yes | 18 | 75 | 200 | PASS | ? |
| italia | `inter` | inter | Internazionale | `/site/paises/italia/equipes/inter` | yes | 14 | 43 | 200 | PASS | ? |
| italia | `italy` | italy | Itália | `/site/paises/italia/equipes/italy` | yes | 44 | 212 | 200 | PASS | ? |
| italia | `jrcasale` | jrcasale | Jrcasale | `/site/paises/italia/equipes/jrcasale` | yes | 2 | 5 | 200 | WARNING | caso historicamente amb?guo |
| italia | `juventus` | juventus | Juventus | `/site/paises/italia/equipes/juventus` | yes | 66 | 523 | 200 | PASS | ? |
| italia | `lazio` | lazio | Lazio | `/site/paises/italia/equipes/lazio` | yes | 13 | 43 | 200 | PASS | ? |
| italia | `lecce` | lecce | Lecce | `/site/paises/italia/equipes/lecce` | yes | 1 | 3 | 200 | PASS | ? |
| italia | `livorno` | livorno | Livorno | `/site/paises/italia/equipes/livorno` | yes | 0 | 2 | 200 | PASS | ? |
| italia | `lucchese` | lucchese | Lucchese | `/site/paises/italia/equipes/lucchese` | yes | 0 | 2 | 200 | PASS | ? |
| italia | `mantova` | mantova | Mantova | `/site/paises/italia/equipes/mantova` | yes | 0 | 2 | 200 | PASS | ? |
| italia | `messina` | messina | Messina | `/site/paises/italia/equipes/messina` | yes | 1 | 8 | 200 | PASS | ? |
| italia | `milan` | milan | Milan | `/site/paises/italia/equipes/milan` | yes | 23 | 60 | 200 | PASS | ? |
| italia | `modena` | modena | Modena | `/site/paises/italia/equipes/modena` | yes | 1 | 3 | 200 | PASS | ? |
| italia | `monza` | monza | Monza | `/site/paises/italia/equipes/monza` | yes | 0 | 4 | 200 | PASS | ? |
| italia | `napoli` | napoli | Napoli | `/site/paises/italia/equipes/napoli` | yes | 30 | 93 | 200 | PASS | ? |
| italia | `novara` | novara | Novara | `/site/paises/italia/equipes/novara` | yes | 2 | 4 | 200 | PASS | ? |
| italia | `padova` | padova | Padova | `/site/paises/italia/equipes/padova` | yes | 2 | 11 | 200 | PASS | ? |
| italia | `palermo` | palermo | Palermo | `/site/paises/italia/equipes/palermo` | yes | 5 | 10 | 200 | PASS | ? |
| italia | `parma` | parma | Parma | `/site/paises/italia/equipes/parma` | yes | 5 | 12 | 200 | PASS | ? |
| italia | `perugia` | perugia | Perugia | `/site/paises/italia/equipes/perugia` | yes | 2 | 15 | 200 | PASS | ? |
| italia | `pescara` | pescara | Pescara | `/site/paises/italia/equipes/pescara` | yes | 2 | 6 | 200 | PASS | ? |
| italia | `piacenza` | piacenza | Piacenza | `/site/paises/italia/equipes/piacenza` | yes | 1 | 5 | 200 | PASS | ? |
| italia | `pisa` | pisa | Pisa | `/site/paises/italia/equipes/pisa` | yes | 1 | 3 | 200 | PASS | ? |
| italia | `provercelli` | provercelli | Pro Vercelli | `/site/paises/italia/equipes/provercelli` | yes | 1 | 2 | 200 | PASS | ? |
| italia | `reggiana` | reggiana | Reggiana | `/site/paises/italia/equipes/reggiana` | yes | 0 | 2 | 200 | PASS | ? |
| italia | `reggina` | reggina | Reggina | `/site/paises/italia/equipes/reggina` | yes | 1 | 3 | 200 | PASS | ? |
| italia | `roma` | roma | Roma | `/site/paises/italia/equipes/roma` | yes | 23 | 73 | 200 | PASS | ? |
| italia | `salernitana` | salernitana | Salernitana | `/site/paises/italia/equipes/salernitana` | yes | 1 | 3 | 200 | PASS | ? |
| italia | `sampdoria` | sampdoria | Sampdoria | `/site/paises/italia/equipes/sampdoria` | yes | 15 | 74 | 200 | PASS | ? |
| italia | `sassari` | sassari | Sassari | `/site/paises/italia/equipes/sassari` | yes | 0 | 3 | 200 | PASS | ? |
| italia | `spal` | spal | SPAL | `/site/paises/italia/equipes/spal` | yes | 3 | 4 | 200 | PASS | ? |
| italia | `taranto` | taranto | Taranto | `/site/paises/italia/equipes/taranto` | yes | 2 | 4 | 200 | PASS | ? |
| italia | `ternana` | ternana | Ternana | `/site/paises/italia/equipes/ternana` | yes | 3 | 5 | 200 | PASS | ? |
| italia | `torino` | torino | Torino | `/site/paises/italia/equipes/torino` | yes | 58 | 655 | 200 | PASS | ? |
| italia | `torres` | torres | Torres | `/site/paises/italia/equipes/torres` | yes | 0 | 3 | 200 | PASS | ? |
| italia | `treviso` | treviso | Treviso | `/site/paises/italia/equipes/treviso` | yes | 0 | 3 | 200 | PASS | ? |
| italia | `udinese` | udinese | Udinese | `/site/paises/italia/equipes/udinese` | yes | 7 | 32 | 200 | PASS | ? |
| italia | `varese` | varese | Varese | `/site/paises/italia/equipes/varese` | yes | 0 | 2 | 200 | PASS | ? |
| italia | `venezia` | venezia | Venezia | `/site/paises/italia/equipes/venezia` | yes | 1 | 9 | 200 | PASS | ? |
| italia | `verona` | verona | Verona | `/site/paises/italia/equipes/verona` | yes | 7 | 11 | 200 | PASS | ? |
| italia | `vicenza` | vicenza | Vicenza | `/site/paises/italia/equipes/vicenza` | yes | 6 | 10 | 200 | PASS | ? |
| outros | `ajax` | ajax | Ajax | `/site/paises/outros/equipes/ajax` | yes | 3 | 5 | 200 | PASS | ? |
| outros | `america-mex` | america_mex | Club América | `/site/paises/outros/equipes/america-mex` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `argentina` | argentina | Argentina | `/site/paises/outros/equipes/argentina` | yes | 3 | 14 | 200 | PASS | ? |
| outros | `argentinos-jrs` | argentinos_jrs | Argentinos Juniors | `/site/paises/outros/equipes/argentinos-jrs` | yes | 0 | 5 | 200 | PASS | ? |
| outros | `arsenal` | arsenal | Arsenal | `/site/paises/outros/equipes/arsenal` | yes | 1 | 3 | 200 | PASS | ? |
| outros | `atletico-col` | atletico_col | Atlético Nacional | `/site/paises/outros/equipes/atletico-col` | yes | 0 | 3 | 200 | PASS | ? |
| outros | `austria` | austria | Áustria | `/site/paises/outros/equipes/austria` | yes | 0 | 3 | 200 | PASS | ? |
| outros | `barcelona` | barcelona | Barcelona | `/site/paises/outros/equipes/barcelona` | yes | 3 | 7 | 200 | PASS | ? |
| outros | `barcelona-equ` | barcelona equ | Barcelona (Equador) | `/site/paises/outros/equipes/barcelona-equ` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `bayern` | bayern | Bayern de Munique | `/site/paises/outros/equipes/bayern` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `benfica` | benfica | Benfica | `/site/paises/outros/equipes/benfica` | yes | 2 | 5 | 200 | PASS | ? |
| outros | `blooming` | blooming | Blooming | `/site/paises/outros/equipes/blooming` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `boavista` | boavista | Boavista | `/site/paises/outros/equipes/boavista` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `boca` | boca | Boca Juniors | `/site/paises/outros/equipes/boca` | yes | 9 | 14 | 200 | PASS | ? |
| outros | `borussia` | borussia | Borussia | `/site/paises/outros/equipes/borussia` | yes | 0 | 2 | 200 | WARNING | caso historicamente amb?guo |
| outros | `bosnia` | bosnia | Bósnia | `/site/paises/outros/equipes/bosnia` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `bulgaria` | bulgaria | Bulgária | `/site/paises/outros/equipes/bulgaria` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `cerro-uru` | cerro uru | Cerro (Uruguai) | `/site/paises/outros/equipes/cerro-uru` | no | 2 | 4 | 200 | WARNING | sem logo; fallback textual funcional |
| outros | `chile` | chile | Chile | `/site/paises/outros/equipes/chile` | yes | 2 | 6 | 200 | PASS | ? |
| outros | `colombia` | colombia | Colômbia | `/site/paises/outros/equipes/colombia` | yes | 1 | 3 | 200 | PASS | ? |
| outros | `cruzazul` | cruzazul | Cruz Azul | `/site/paises/outros/equipes/cruzazul` | yes | 1 | 7 | 200 | PASS | ? |
| outros | `cucuta` | cucuta | Cúcuta Deportivo | `/site/paises/outros/equipes/cucuta` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `czechoslovakia` | czechoslovakia | Tchecoslováquia | `/site/paises/outros/equipes/czechoslovakia` | yes | 0 | 6 | 200 | PASS | ? |
| outros | `dinamo` | dinamo | Dinamo | `/site/paises/outros/equipes/dinamo` | yes | 0 | 2 | 200 | WARNING | caso historicamente amb?guo |
| outros | `england` | england | Inglaterra | `/site/paises/outros/equipes/england` | yes | 3 | 9 | 200 | PASS | ? |
| outros | `estudiantes` | estudiantes | Estudiantes | `/site/paises/outros/equipes/estudiantes` | yes | 1 | 4 | 200 | PASS | ? |
| outros | `france` | france | França | `/site/paises/outros/equipes/france` | yes | 1 | 3 | 200 | PASS | ? |
| outros | `germany` | germany | Alemanha | `/site/paises/outros/equipes/germany` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `ghana` | ghana | Gana | `/site/paises/outros/equipes/ghana` | yes | 0 | 4 | 200 | PASS | ? |
| outros | `haka` | haka | Haka | `/site/paises/outros/equipes/haka` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `holanda` | holanda | Holanda | `/site/paises/outros/equipes/holanda` | yes | 1 | 3 | 200 | PASS | ? |
| outros | `independiente` | independiente | Independiente | `/site/paises/outros/equipes/independiente` | yes | 1 | 3 | 200 | PASS | ? |
| outros | `israel` | israel | Israel | `/site/paises/outros/equipes/israel` | yes | 1 | 3 | 200 | PASS | ? |
| outros | `japao` | japao | Japão | `/site/paises/outros/equipes/japao` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `macedonia` | macedonia | Macedônia | `/site/paises/outros/equipes/macedonia` | yes | 1 | 3 | 200 | PASS | ? |
| outros | `manchester` | manchester | Manchester United | `/site/paises/outros/equipes/manchester` | yes | 2 | 6 | 200 | PASS | ? |
| outros | `manchester-city` | manchester city | Manchester City | `/site/paises/outros/equipes/manchester-city` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `mexico` | mexico | México | `/site/paises/outros/equipes/mexico` | yes | 3 | 4 | 200 | PASS | ? |
| outros | `olimpia` | olimpia | Olimpia | `/site/paises/outros/equipes/olimpia` | yes | 1 | 5 | 200 | PASS | ? |
| outros | `penarol` | penarol | Peñarol | `/site/paises/outros/equipes/penarol` | yes | 0 | 3 | 200 | PASS | ? |
| outros | `peru` | peru | Peru | `/site/paises/outros/equipes/peru` | yes | 1 | 4 | 200 | PASS | ? |
| outros | `polonia` | polonia | Polônia | `/site/paises/outros/equipes/polonia` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `porto` | porto | Porto | `/site/paises/outros/equipes/porto` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `portugal` | portugal | Portugal | `/site/paises/outros/equipes/portugal` | yes | 0 | 3 | 200 | PASS | ? |
| outros | `qatar` | qatar | Catar | `/site/paises/outros/equipes/qatar` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `queretaro` | queretaro | Querétaro | `/site/paises/outros/equipes/queretaro` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `real` | real | Real Madrid | `/site/paises/outros/equipes/real` | yes | 1 | 5 | 200 | PASS | ? |
| outros | `riverplate` | riverplate | River Plate | `/site/paises/outros/equipes/riverplate` | yes | 1 | 4 | 200 | PASS | ? |
| outros | `romania` | romania | Romênia | `/site/paises/outros/equipes/romania` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `rosario` | rosario | Rosario | `/site/paises/outros/equipes/rosario` | yes | 1 | 2 | 200 | WARNING | caso historicamente amb?guo |
| outros | `russia` | russia | Rússia | `/site/paises/outros/equipes/russia` | yes | 2 | 2 | 200 | PASS | ? |
| outros | `sanjose` | sanjose | Sanjose | `/site/paises/outros/equipes/sanjose` | yes | 0 | 4 | 200 | WARNING | caso historicamente amb?guo |
| outros | `servia` | servia | Sérvia | `/site/paises/outros/equipes/servia` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `sovietunion` | sovietunion | União Soviética | `/site/paises/outros/equipes/sovietunion` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `spain` | spain | Espanha | `/site/paises/outros/equipes/spain` | yes | 2 | 4 | 200 | PASS | ? |
| outros | `sparta` | sparta | Sparta | `/site/paises/outros/equipes/sparta` | yes | 1 | 2 | 200 | WARNING | caso historicamente amb?guo |
| outros | `sportinglisboa` | sportinglisboa | Sporting CP | `/site/paises/outros/equipes/sportinglisboa` | no | 0 | 5 | 200 | WARNING | sem logo; fallback textual funcional |
| outros | `strongest` | strongest | The Strongest | `/site/paises/outros/equipes/strongest` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `suecia` | suecia | Suécia | `/site/paises/outros/equipes/suecia` | yes | 1 | 3 | 200 | PASS | ? |
| outros | `switzerland` | switzerland | Suíça | `/site/paises/outros/equipes/switzerland` | yes | 1 | 2 | 200 | PASS | ? |
| outros | `turkey` | turkey | Turquia | `/site/paises/outros/equipes/turkey` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `universidad-chile` | universidad_chile | Universidad de Chile | `/site/paises/outros/equipes/universidad-chile` | no | 1 | 2 | 200 | WARNING | sem logo; fallback textual funcional |
| outros | `uruguai` | uruguai | Uruguai | `/site/paises/outros/equipes/uruguai` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `velez` | velez | Vélez Sarsfield | `/site/paises/outros/equipes/velez` | yes | 0 | 2 | 200 | PASS | ? |
| outros | `venezuela` | venezuela | Venezuela | `/site/paises/outros/equipes/venezuela` | yes | 2 | 3 | 200 | PASS | ? |
| outros | `vitoria-setubal-por` | vitoria_setubal_por | Vitória de Setúbal | `/site/paises/outros/equipes/vitoria-setubal-por` | no | 1 | 2 | 200 | WARNING | sem logo; fallback textual funcional |
| outros | `widzew-lodz` | widzew lodz | Widzew Łódź | `/site/paises/outros/equipes/widzew-lodz` | yes | 1 | 2 | 200 | PASS | ? |

## Ap?ndice B ? 352 cole??es vazias

- `/site/paises/brasil/equipes/america-rj/collections/08-23`
- `/site/paises/brasil/equipes/atletico/collections/01-18`
- `/site/paises/brasil/equipes/atletico/collections/01-19`
- `/site/paises/brasil/equipes/atletico/collections/01-20`
- `/site/paises/brasil/equipes/atletico/collections/01-26`
- `/site/paises/brasil/equipes/atletico/collections/02-13`
- `/site/paises/brasil/equipes/atletico/collections/02-17`
- `/site/paises/brasil/equipes/atletico/collections/02-22`
- `/site/paises/brasil/equipes/atletico/collections/02-25`
- `/site/paises/brasil/equipes/atletico/collections/03-14-2`
- `/site/paises/brasil/equipes/atletico/collections/03-16`
- `/site/paises/brasil/equipes/atletico/collections/03-19`
- `/site/paises/brasil/equipes/atletico/collections/03-20`
- `/site/paises/brasil/equipes/atletico/collections/03-23`
- `/site/paises/brasil/equipes/atletico/collections/03-25`
- `/site/paises/brasil/equipes/atletico/collections/04-16`
- `/site/paises/brasil/equipes/atletico/collections/04-20`
- `/site/paises/brasil/equipes/atletico/collections/05-24`
- `/site/paises/brasil/equipes/atletico/collections/06-13`
- `/site/paises/brasil/equipes/atletico/collections/06-14`
- `/site/paises/brasil/equipes/atletico/collections/06-16`
- `/site/paises/brasil/equipes/atletico/collections/07-13`
- `/site/paises/brasil/equipes/atletico/collections/07-22`
- `/site/paises/brasil/equipes/atletico/collections/07-25-2`
- `/site/paises/brasil/equipes/atletico/collections/08-14`
- `/site/paises/brasil/equipes/atletico/collections/08-14-2`
- `/site/paises/brasil/equipes/atletico/collections/08-18`
- `/site/paises/brasil/equipes/atletico/collections/08-18-2`
- `/site/paises/brasil/equipes/atletico/collections/08-23`
- `/site/paises/brasil/equipes/atletico/collections/09-18`
- `/site/paises/brasil/equipes/atletico/collections/09-24`
- `/site/paises/brasil/equipes/atletico/collections/09-24-2`
- `/site/paises/brasil/equipes/atletico/collections/10-18`
- `/site/paises/brasil/equipes/atletico/collections/10-19`
- `/site/paises/brasil/equipes/atletico/collections/11-13`
- `/site/paises/brasil/equipes/atletico/collections/11-17`
- `/site/paises/brasil/equipes/atletico/collections/11-22`
- `/site/paises/brasil/equipes/atleticop/collections/11-21`
- `/site/paises/brasil/equipes/bahia/collections/01-20`
- `/site/paises/brasil/equipes/bahia/collections/02-17`
- `/site/paises/brasil/equipes/bahia/collections/03-19`
- `/site/paises/brasil/equipes/bahia/collections/09-22`
- `/site/paises/brasil/equipes/botafogo/collections/01-18`
- `/site/paises/brasil/equipes/botafogo/collections/03-15`
- `/site/paises/brasil/equipes/botafogo/collections/03-19`
- `/site/paises/brasil/equipes/botafogo/collections/11-21`
- `/site/paises/brasil/equipes/capivariano/collections/01-26`
- `/site/paises/brasil/equipes/chapecoense/collections/01-18`
- `/site/paises/brasil/equipes/chapecoense/collections/01-20`
- `/site/paises/brasil/equipes/chapecoense/collections/08-17`
- `/site/paises/brasil/equipes/corinthians/collections/01-16`
- `/site/paises/brasil/equipes/corinthians/collections/01-18`
- `/site/paises/brasil/equipes/corinthians/collections/01-20`
- `/site/paises/brasil/equipes/corinthians/collections/02-17`
- `/site/paises/brasil/equipes/corinthians/collections/03-15`
- `/site/paises/brasil/equipes/corinthians/collections/03-16`
- `/site/paises/brasil/equipes/corinthians/collections/03-20`
- `/site/paises/brasil/equipes/corinthians/collections/04-16`
- `/site/paises/brasil/equipes/corinthians/collections/05-15`
- `/site/paises/brasil/equipes/corinthians/collections/06-16`
- `/site/paises/brasil/equipes/corinthians/collections/07-18`
- `/site/paises/brasil/equipes/corinthians/collections/08-17`
- `/site/paises/brasil/equipes/corinthians/collections/08-18`
- `/site/paises/brasil/equipes/corinthians/collections/09-18`
- `/site/paises/brasil/equipes/corinthians/collections/10-18`
- `/site/paises/brasil/equipes/corinthians/collections/11-17`
- `/site/paises/brasil/equipes/corinthians/collections/11-18`
- `/site/paises/brasil/equipes/corinthians/collections/11-21`
- `/site/paises/brasil/equipes/corinthians/collections/11-21-2`
- `/site/paises/brasil/equipes/cruzeiro/collections/01-16`
- `/site/paises/brasil/equipes/cruzeiro/collections/01-26`
- `/site/paises/brasil/equipes/cruzeiro/collections/03-16`
- `/site/paises/brasil/equipes/cruzeiro/collections/03-17`
- `/site/paises/brasil/equipes/cruzeiro/collections/04-20`
- `/site/paises/brasil/equipes/cruzeiro/collections/07-17`
- `/site/paises/brasil/equipes/cruzeiro/collections/08-14`
- `/site/paises/brasil/equipes/cruzeiro/collections/08-18`
- `/site/paises/brasil/equipes/cruzeiro/collections/09-18`
- `/site/paises/brasil/equipes/cruzeiro/collections/11-17`
- `/site/paises/brasil/equipes/csa/collections/07-25`
- `/site/paises/brasil/equipes/flamengo/collections/01-20`
- `/site/paises/brasil/equipes/flamengo/collections/07-22`
- `/site/paises/brasil/equipes/flamengo/collections/08-14`
- `/site/paises/brasil/equipes/flamengo/collections/08-18`
- `/site/paises/brasil/equipes/flamengo/collections/09-22`
- `/site/paises/brasil/equipes/fluminense/collections/06-16`
- `/site/paises/brasil/equipes/fluminense/collections/07-22`
- `/site/paises/brasil/equipes/fluminense/collections/09-24`
- `/site/paises/brasil/equipes/fluminense/collections/11-17`
- `/site/paises/brasil/equipes/gremio/collections/01-18`
- `/site/paises/brasil/equipes/gremio/collections/01-19`
- `/site/paises/brasil/equipes/gremio/collections/01-20`
- `/site/paises/brasil/equipes/gremio/collections/02-17`
- `/site/paises/brasil/equipes/gremio/collections/03-19`
- `/site/paises/brasil/equipes/gremio/collections/03-20`
- `/site/paises/brasil/equipes/gremio/collections/03-25`
- `/site/paises/brasil/equipes/gremio/collections/04-16`
- `/site/paises/brasil/equipes/gremio/collections/04-20`
- `/site/paises/brasil/equipes/gremio/collections/06-18`
- `/site/paises/brasil/equipes/gremio/collections/08-14-2`
- `/site/paises/brasil/equipes/gremio/collections/08-18`
- `/site/paises/brasil/equipes/gremio/collections/09-18`
- `/site/paises/brasil/equipes/gremio/collections/10-18`
- `/site/paises/brasil/equipes/gremio/collections/11-17`
- `/site/paises/brasil/equipes/gremio/collections/11-21`
- `/site/paises/brasil/equipes/internacional/collections/01-24`
- `/site/paises/brasil/equipes/internacional/collections/03-15`
- `/site/paises/brasil/equipes/internacional/collections/03-16`
- `/site/paises/brasil/equipes/internacional/collections/03-23`
- `/site/paises/brasil/equipes/internacional/collections/04-14`
- `/site/paises/brasil/equipes/internacional/collections/05-15`
- `/site/paises/brasil/equipes/internacional/collections/08-23`
- `/site/paises/brasil/equipes/internacional/collections/09-23`
- `/site/paises/brasil/equipes/internacional/collections/11-14`
- `/site/paises/brasil/equipes/internacional/collections/11-17`
- `/site/paises/brasil/equipes/londrina/collections/11-21`
- `/site/paises/brasil/equipes/palmeiras/collections/01-18`
- `/site/paises/brasil/equipes/palmeiras/collections/01-19`
- `/site/paises/brasil/equipes/palmeiras/collections/01-20`
- `/site/paises/brasil/equipes/palmeiras/collections/02-17`
- `/site/paises/brasil/equipes/palmeiras/collections/03-15`
- `/site/paises/brasil/equipes/palmeiras/collections/03-16`
- `/site/paises/brasil/equipes/palmeiras/collections/03-17`
- `/site/paises/brasil/equipes/palmeiras/collections/03-19`
- `/site/paises/brasil/equipes/palmeiras/collections/04-14-copia`
- `/site/paises/brasil/equipes/palmeiras/collections/04-15`
- `/site/paises/brasil/equipes/palmeiras/collections/04-15-copia`
- `/site/paises/brasil/equipes/palmeiras/collections/04-16`
- `/site/paises/brasil/equipes/palmeiras/collections/05-15`
- `/site/paises/brasil/equipes/palmeiras/collections/06-14`
- `/site/paises/brasil/equipes/palmeiras/collections/07-25`
- `/site/paises/brasil/equipes/palmeiras/collections/08-14`
- `/site/paises/brasil/equipes/palmeiras/collections/08-18`
- `/site/paises/brasil/equipes/palmeiras/collections/09-18`
- `/site/paises/brasil/equipes/palmeiras/collections/11-14`
- `/site/paises/brasil/equipes/palmeiras/collections/11-17`
- `/site/paises/brasil/equipes/palmeiras/collections/11-21`
- `/site/paises/brasil/equipes/santos/collections/01-16`
- `/site/paises/brasil/equipes/santos/collections/01-18`
- `/site/paises/brasil/equipes/santos/collections/01-19`
- `/site/paises/brasil/equipes/santos/collections/01-20`
- `/site/paises/brasil/equipes/santos/collections/02-22`
- `/site/paises/brasil/equipes/santos/collections/03-15`
- `/site/paises/brasil/equipes/santos/collections/03-17`
- `/site/paises/brasil/equipes/santos/collections/03-19`
- `/site/paises/brasil/equipes/santos/collections/04-15`
- `/site/paises/brasil/equipes/santos/collections/05-24`
- `/site/paises/brasil/equipes/santos/collections/07-13`
- `/site/paises/brasil/equipes/santos/collections/07-18`
- `/site/paises/brasil/equipes/santos/collections/08-14`
- `/site/paises/brasil/equipes/santos/collections/10-18`
- `/site/paises/brasil/equipes/santos/collections/10-19`
- `/site/paises/brasil/equipes/santos/collections/11-13`
- `/site/paises/brasil/equipes/santos/collections/11-14`
- `/site/paises/brasil/equipes/santos/collections/11-17`
- `/site/paises/brasil/equipes/santos/collections/11-17-2`
- `/site/paises/brasil/equipes/santos/collections/11-21`
- `/site/paises/brasil/equipes/saopaulo/collections/01-18`
- `/site/paises/brasil/equipes/saopaulo/collections/03-15`
- `/site/paises/brasil/equipes/saopaulo/collections/03-16`
- `/site/paises/brasil/equipes/saopaulo/collections/03-25`
- `/site/paises/brasil/equipes/saopaulo/collections/04-14`
- `/site/paises/brasil/equipes/saopaulo/collections/04-15`
- `/site/paises/brasil/equipes/saopaulo/collections/07-22`
- `/site/paises/brasil/equipes/saopaulo/collections/11-13`
- `/site/paises/brasil/equipes/saopaulo/collections/11-17`
- `/site/paises/brasil/equipes/saopaulo/collections/11-18`
- `/site/paises/brasil/equipes/sport/collections/11-17`
- `/site/paises/brasil/equipes/xvpira/collections/08-22`
- `/site/paises/brasil/equipes/xvpira/collections/09-22`
- `/site/paises/italia/equipes/bologna/collections/04-20`
- `/site/paises/italia/equipes/bologna/collections/07-25`
- `/site/paises/italia/equipes/cagliari/collections/01-14`
- `/site/paises/italia/equipes/cagliari/collections/03-17`
- `/site/paises/italia/equipes/cagliari/collections/03-23`
- `/site/paises/italia/equipes/cagliari/collections/06-23`
- `/site/paises/italia/equipes/cagliari/collections/07-13`
- `/site/paises/italia/equipes/cagliari/collections/07-17`
- `/site/paises/italia/equipes/cagliari/collections/07-25`
- `/site/paises/italia/equipes/cagliari/collections/08-17`
- `/site/paises/italia/equipes/cagliari/collections/08-22`
- `/site/paises/italia/equipes/cagliari/collections/09-15`
- `/site/paises/italia/equipes/cagliari/collections/09-24`
- `/site/paises/italia/equipes/cagliari/collections/09-24-2`
- `/site/paises/italia/equipes/cagliari/collections/11-21`
- `/site/paises/italia/equipes/chievo/collections/03-14`
- `/site/paises/italia/equipes/chievo/collections/03-19-2`
- `/site/paises/italia/equipes/chievo/collections/04-20`
- `/site/paises/italia/equipes/chievo/collections/06-14`
- `/site/paises/italia/equipes/chievo/collections/06-14-2`
- `/site/paises/italia/equipes/chievo/collections/06-18`
- `/site/paises/italia/equipes/chievo/collections/06-18-2`
- `/site/paises/italia/equipes/chievo/collections/08-17`
- `/site/paises/italia/equipes/chievo/collections/09-18`
- `/site/paises/italia/equipes/chievo/collections/10-19`
- `/site/paises/italia/equipes/fiorentina/collections/01-26`
- `/site/paises/italia/equipes/fiorentina/collections/02-17`
- `/site/paises/italia/equipes/fiorentina/collections/02-25`
- `/site/paises/italia/equipes/fiorentina/collections/04-16`
- `/site/paises/italia/equipes/fiorentina/collections/04-20`
- `/site/paises/italia/equipes/fiorentina/collections/06-14`
- `/site/paises/italia/equipes/fiorentina/collections/06-16`
- `/site/paises/italia/equipes/fiorentina/collections/07-17`
- `/site/paises/italia/equipes/fiorentina/collections/07-25`
- `/site/paises/italia/equipes/fiorentina/collections/08-18`
- `/site/paises/italia/equipes/fiorentina/collections/09-18`
- `/site/paises/italia/equipes/fiorentina/collections/09-23`
- `/site/paises/italia/equipes/fiorentina/collections/09-24`
- `/site/paises/italia/equipes/genoa/collections/07-18`
- `/site/paises/italia/equipes/genoa/collections/07-22`
- `/site/paises/italia/equipes/genoa/collections/09-24`
- `/site/paises/italia/equipes/inter/collections/07-25`
- `/site/paises/italia/equipes/inter/collections/11-23`
- `/site/paises/italia/equipes/italy/collections/01-14`
- `/site/paises/italia/equipes/italy/collections/03-14`
- `/site/paises/italia/equipes/italy/collections/03-14-2`
- `/site/paises/italia/equipes/italy/collections/03-19`
- `/site/paises/italia/equipes/italy/collections/03-19-2`
- `/site/paises/italia/equipes/italy/collections/04-14`
- `/site/paises/italia/equipes/italy/collections/04-20`
- `/site/paises/italia/equipes/italy/collections/06-18`
- `/site/paises/italia/equipes/italy/collections/07-18`
- `/site/paises/italia/equipes/italy/collections/08-17`
- `/site/paises/italia/equipes/italy/collections/08-18`
- `/site/paises/italia/equipes/italy/collections/08-18-2`
- `/site/paises/italia/equipes/italy/collections/09-12`
- `/site/paises/italia/equipes/italy/collections/09-15`
- `/site/paises/italia/equipes/italy/collections/10-10`
- `/site/paises/italia/equipes/italy/collections/10-19`
- `/site/paises/italia/equipes/italy/collections/11-21`
- `/site/paises/italia/equipes/juventus/collections/01-24`
- `/site/paises/italia/equipes/juventus/collections/02-13`
- `/site/paises/italia/equipes/juventus/collections/02-15`
- `/site/paises/italia/equipes/juventus/collections/02-22`
- `/site/paises/italia/equipes/juventus/collections/03-14`
- `/site/paises/italia/equipes/juventus/collections/03-14-2`
- `/site/paises/italia/equipes/juventus/collections/03-16`
- `/site/paises/italia/equipes/juventus/collections/03-17`
- `/site/paises/italia/equipes/juventus/collections/03-19`
- `/site/paises/italia/equipes/juventus/collections/03-20`
- `/site/paises/italia/equipes/juventus/collections/03-25`
- `/site/paises/italia/equipes/juventus/collections/04-14`
- `/site/paises/italia/equipes/juventus/collections/04-15`
- `/site/paises/italia/equipes/juventus/collections/04-16`
- `/site/paises/italia/equipes/juventus/collections/04-20`
- `/site/paises/italia/equipes/juventus/collections/04-21`
- `/site/paises/italia/equipes/juventus/collections/05-15`
- `/site/paises/italia/equipes/juventus/collections/06-18-2`
- `/site/paises/italia/equipes/juventus/collections/06-23`
- `/site/paises/italia/equipes/juventus/collections/07-13`
- `/site/paises/italia/equipes/juventus/collections/07-13-2`
- `/site/paises/italia/equipes/juventus/collections/07-17`
- `/site/paises/italia/equipes/juventus/collections/08-14`
- `/site/paises/italia/equipes/juventus/collections/08-17`
- `/site/paises/italia/equipes/juventus/collections/08-18`
- `/site/paises/italia/equipes/juventus/collections/08-18-2`
- `/site/paises/italia/equipes/juventus/collections/08-18-3`
- `/site/paises/italia/equipes/juventus/collections/08-22`
- `/site/paises/italia/equipes/juventus/collections/09-15`
- `/site/paises/italia/equipes/juventus/collections/09-23`
- `/site/paises/italia/equipes/juventus/collections/09-23-2`
- `/site/paises/italia/equipes/juventus/collections/09-24-2`
- `/site/paises/italia/equipes/juventus/collections/11-14`
- `/site/paises/italia/equipes/juventus/collections/11-22`
- `/site/paises/italia/equipes/juventus/collections/11-23`
- `/site/paises/italia/equipes/juventus/collections/12-14`
- `/site/paises/italia/equipes/juventus/collections/12-17`
- `/site/paises/italia/equipes/juventus/collections/12-25`
- `/site/paises/italia/equipes/juventus/collections/50-60`
- `/site/paises/italia/equipes/juventus/collections/70-80`
- `/site/paises/italia/equipes/juventus/collections/80-90`
- `/site/paises/italia/equipes/lazio/collections/02-13`
- `/site/paises/italia/equipes/lazio/collections/08-22`
- `/site/paises/italia/equipes/milan/collections/04-16`
- `/site/paises/italia/equipes/milan/collections/07-18`
- `/site/paises/italia/equipes/milan/collections/07-19`
- `/site/paises/italia/equipes/milan/collections/09-23`
- `/site/paises/italia/equipes/milan/collections/12-17`
- `/site/paises/italia/equipes/napoli/collections/03-15`
- `/site/paises/italia/equipes/napoli/collections/03-17`
- `/site/paises/italia/equipes/napoli/collections/03-19-2`
- `/site/paises/italia/equipes/napoli/collections/03-25`
- `/site/paises/italia/equipes/napoli/collections/04-16`
- `/site/paises/italia/equipes/napoli/collections/04-21`
- `/site/paises/italia/equipes/napoli/collections/05-09`
- `/site/paises/italia/equipes/napoli/collections/05-24`
- `/site/paises/italia/equipes/napoli/collections/06-18`
- `/site/paises/italia/equipes/napoli/collections/09-24`
- `/site/paises/italia/equipes/napoli/collections/10-13`
- `/site/paises/italia/equipes/napoli/collections/11-22`
- `/site/paises/italia/equipes/novara/collections/08-17`
- `/site/paises/italia/equipes/parma/collections/07-17`
- `/site/paises/italia/equipes/roma/collections/02-17`
- `/site/paises/italia/equipes/roma/collections/02-25`
- `/site/paises/italia/equipes/roma/collections/03-20`
- `/site/paises/italia/equipes/roma/collections/03-23`
- `/site/paises/italia/equipes/roma/collections/04-21`
- `/site/paises/italia/equipes/roma/collections/07-18`
- `/site/paises/italia/equipes/roma/collections/09-23`
- `/site/paises/italia/equipes/sampdoria/collections/05-24`
- `/site/paises/italia/equipes/taranto/collections/08-16`
- `/site/paises/italia/equipes/torino/collections/01-14`
- `/site/paises/italia/equipes/torino/collections/01-20`
- `/site/paises/italia/equipes/torino/collections/02-16`
- `/site/paises/italia/equipes/torino/collections/02-17`
- `/site/paises/italia/equipes/torino/collections/02-22`
- `/site/paises/italia/equipes/torino/collections/03-14-2`
- `/site/paises/italia/equipes/torino/collections/03-15-2`
- `/site/paises/italia/equipes/torino/collections/03-19`
- `/site/paises/italia/equipes/torino/collections/03-19-2`
- `/site/paises/italia/equipes/torino/collections/03-20`
- `/site/paises/italia/equipes/torino/collections/03-25`
- `/site/paises/italia/equipes/torino/collections/04-15`
- `/site/paises/italia/equipes/torino/collections/04-20`
- `/site/paises/italia/equipes/torino/collections/05-23`
- `/site/paises/italia/equipes/torino/collections/05-24`
- `/site/paises/italia/equipes/torino/collections/06-23`
- `/site/paises/italia/equipes/torino/collections/07-13`
- `/site/paises/italia/equipes/torino/collections/07-13-2`
- `/site/paises/italia/equipes/torino/collections/07-13-3`
- `/site/paises/italia/equipes/torino/collections/07-17`
- `/site/paises/italia/equipes/torino/collections/07-18`
- `/site/paises/italia/equipes/torino/collections/08-16`
- `/site/paises/italia/equipes/torino/collections/08-18`
- `/site/paises/italia/equipes/torino/collections/08-18-2`
- `/site/paises/italia/equipes/torino/collections/08-18-3`
- `/site/paises/italia/equipes/torino/collections/09-15`
- `/site/paises/italia/equipes/torino/collections/09-24`
- `/site/paises/italia/equipes/torino/collections/10-13`
- `/site/paises/italia/equipes/torino/collections/10-19`
- `/site/paises/italia/equipes/torino/collections/11-21`
- `/site/paises/italia/equipes/torino/collections/11-21-2`
- `/site/paises/italia/equipes/torino/collections/12-17`
- `/site/paises/italia/equipes/torino/collections/20-30`
- `/site/paises/italia/equipes/torino/collections/60-70`
- `/site/paises/italia/equipes/torino/collections/70-80`
- `/site/paises/italia/equipes/torino/collections/80-90`
- `/site/paises/italia/equipes/torino/collections/fot-gio`
- `/site/paises/italia/equipes/udinese/collections/10-19`
- `/site/paises/italia/equipes/verona/collections/10-19`
- `/site/paises/italia/equipes/vicenza/collections/02-25`
- `/site/paises/italia/equipes/vicenza/collections/04-20`
- `/site/paises/outros/equipes/argentina/collections/notes`
- `/site/paises/outros/equipes/boca/collections/03-20`
- `/site/paises/outros/equipes/boca/collections/09-24`
- `/site/paises/outros/equipes/boca/collections/notes`
- `/site/paises/outros/equipes/cerro-uru/collections/03-19`
- `/site/paises/outros/equipes/manchester/collections/01-24`
- `/site/paises/outros/equipes/mexico/collections/03-15`
- `/site/paises/outros/equipes/mexico/collections/08-14`
- `/site/paises/outros/equipes/russia/collections/07-25`
- `/site/paises/outros/equipes/venezuela/collections/06-16`

## Ap?ndice C ? 8 itens sem m?dia

- `/site/items/brasil/teams/atletico/items/1988`
- `/site/items/brasil/teams/corinthians/collections/04-09/1985`
- `/site/items/brasil/teams/selecaob/items/1972-fc0de5`
- `/site/items/brasil/teams/selecaob/items/2006-8f3c3d`
- `/site/items/italia/teams/bologna/items/documento-sem-titulo`
- `/site/items/italia/teams/juventus/items/1944-1945`
- `/site/items/italia/teams/sassari/items/1988-1989`
- `/site/items/italia/teams/ternana/items/2002`

## Integridade read-only e Git

- Nenhuma corre??o foi executada.
- Nenhum c?digo, CSS, asset, dado, banco, API, workspace ou camada derivada foi alterado/reconstru?do.
- ?nico arquivo autorizado criado/alterado: `docs/public-site-homologation-audit.md`.
- Build gerou somente conte?do transit?rio em `frontend/dist`; nenhum artefato foi adicionado deliberadamente ao controle de vers?o.
- Nenhum commit e nenhum push foram realizados.

