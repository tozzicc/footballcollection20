import assert from 'node:assert/strict'
import test from 'node:test'
import { mergePublicSearchResults, normalizePublicSearchTerm, publicSearchApiQueries, publicSearchResultText } from './publicSearch.ts'

const team=(countrySlug,slug,name)=>({countrySlug,slug,name,collectionsCount:1,itemsCount:1,imagesCount:1,latestInclusionPeriod:null,primaryMedia:null,logoMedia:null})
const teams=[team('brasil','atletico','atletico'),team('brasil','atleticop','atleticop'),team('brasil','america-mg','america_mg'),team('brasil','america-rn','america_rn'),team('brasil','america-rj','america_rj'),team('brasil','gremio','gremio'),team('brasil','saopaulo','saopaulo'),team('brasil','selecaob','selecaob'),team('brasil','caxias','caxias'),team('brasil','chapecoense','chapecoense'),team('brasil','coritiba','coritiba'),team('brasil','ituano','ituano'),team('italia','juventus','juventus')]
const empty={items:[],total:0,limit:24,offset:0,hasNext:false}
const item=(teamSlug,title,publicRoute=`/items/brasil/teams/${teamSlug}/items/${title.toLocaleLowerCase().replaceAll(' ','-')}`)=>({type:'item',title,subtitle:title.toLocaleUpperCase(),countrySlug:'brasil',teamSlug,publicRoute,primaryMedia:null})

test('normaliza acentos, hífens e espaços',()=>assert.equal(normalizePublicSearchTerm('  Atlético-MG '),'atletico mg'))
test('encontra display names com e sem acento',()=>{
 assert.equal(mergePublicSearchResults('Atlético-MG',empty,teams).items[0].teamSlug,'atletico')
 assert.equal(mergePublicSearchResults('Gremio',empty,teams).items[0].teamSlug,'gremio')
 assert.equal(mergePublicSearchResults('Sao Paulo',empty,teams).items[0].teamSlug,'saopaulo')
})
test('retorna somente as equipes que compartilham o nome América',()=>{
 const api={...empty,items:[item('america-mg','América MG'),item('america-rj','América - RJ')]}
 const result=mergePublicSearchResults('América',api,teams)
 assert.deepEqual(result.items.map(x=>x.teamSlug),['america-mg','america-rn','america-rj'])
 assert.equal(result.items.every(x=>x.type==='team'),true)
})
test('inclui Chicão como resultado editorial, sem convertê-lo em item',()=>assert.deepEqual(mergePublicSearchResults('Chicao',empty,teams).items[0],{type:'editorial',title:'Chicão — O Deus da Raça',subtitle:'Homenagem',publicRoute:'/site/chicao',primaryMedia:null}))
test('equipe exata elimina conteúdo e remove entidade duplicada da API',()=>{
 const api={...empty,items:[{type:'team',title:'atletico',countrySlug:'brasil',teamSlug:'atletico',primaryMedia:null},{type:'item',title:'Atlético',countrySlug:'brasil',teamSlug:'atletico',publicRoute:'/items/x',primaryMedia:null}]}
 const result=mergePublicSearchResults('atletico',api,teams)
 assert.equal(result.items.filter(x=>x.type==='team'&&x.teamSlug==='atletico').length,1)
 assert.equal(result.items.filter(x=>x.type==='item').length,0)
})
test('retorna somente a entidade São Paulo com e sem acento',()=>{
 const api={...empty,items:[item('caxias','São Paulo'),item('chapecoense','São Paulo'),item('coritiba','São Paulo'),item('ituano','São Paulo'),item('saopaulo','São Paulo')]}
 for(const query of ['São Paulo','Sao Paulo']){
  const result=mergePublicSearchResults(query,api,teams)
  assert.deepEqual(result.items.map(x=>[x.type,x.teamSlug]),[['team','saopaulo']])
  assert.equal(result.items.some(x=>['caxias','chapecoense','coritiba','ituano'].includes(x.teamSlug)),false)
 }
})
test('apresenta item com a equipe real sem identidade textual enganosa',()=>{
 assert.deepEqual(publicSearchResultText(item('caxias','São Paulo'),teams),{title:'São Paulo',subtitle:'Equipe: Caxias'})
 assert.deepEqual(publicSearchResultText(item('chapecoense','São Paulo'),teams),{title:'São Paulo',subtitle:'Equipe: Chapecoense'})
})
test('prioriza identidades exatas e preserva identidades parciais',()=>{
 for(const [query,slug] of [['Atlético-MG','atletico'],['Atletico-MG','atletico'],['América-MG','america-mg'],['America-MG','america-mg'],['Grêmio','gremio'],['Gremio','gremio'],['Juventus','juventus']])assert.equal(mergePublicSearchResults(query,empty,teams).items[0].teamSlug,slug)
 assert.deepEqual(mergePublicSearchResults('América',empty,teams).items.map(x=>x.teamSlug),['america-mg','america-rn','america-rj'])
 assert.deepEqual(mergePublicSearchResults('Atlético',empty,teams).items.map(x=>x.teamSlug),['atletico'])
})
test('restringe identidade exata somente à entidade da equipe',()=>{
 const api={...empty,items:[item('atletico','Atlético Mineiro'),item('atleticop','Atlético-MG')]}
 for(const query of ['Atlético-MG','Atletico-MG'])assert.deepEqual(mergePublicSearchResults(query,api,teams).items.map(x=>x.teamSlug),['atletico'])
 const americaApi={...empty,items:[item('america-mg','América-MG'),item('america-rj','América-MG')]}
 for(const query of ['América-MG','America-MG'])assert.deepEqual(mergePublicSearchResults(query,americaApi,teams).items.map(x=>x.teamSlug),['america-mg'])
 const gremioApi={...empty,items:[item('gremio','Grêmio'),item('caxias','Grêmio')]}
 for(const query of ['Grêmio','Gremio'])assert.deepEqual(mergePublicSearchResults(query,gremioApi,teams).items.map(x=>x.teamSlug),['gremio'])
})
test('preserva busca genérica e ausência de resultado artificial',()=>{
 const generic={...empty,items:[item('juventus','Campeonato Italiano')]}
 assert.equal(mergePublicSearchResults('Campeonato',generic,teams).items[0].title,'Campeonato Italiano')
 assert.equal(mergePublicSearchResults('termo seguramente inexistente',empty,teams).items.length,0)
 const brasil={...empty,items:[item('caxias','Brasil')]}
 assert.equal(mergePublicSearchResults('Brasil',brasil,teams).items[0].type,'item')
})
test('usa o display name como consulta complementar quando a API não normaliza acentos',()=>{
 assert.deepEqual(publicSearchApiQueries('Sao Paulo',teams),['Sao Paulo','São Paulo'])
 assert.deepEqual(publicSearchApiQueries('Gremio',teams),['Gremio','Grêmio'])
 assert.deepEqual(publicSearchApiQueries('São Paulo',teams),['São Paulo'])
})
