type TeamIdentity={countrySlug?:string|null;slug?:string|null;name?:string|null}

const overrides:Record<string,string>={
 'brasil/america-mg':'América-MG','brasil/america-rj':'América-RJ','brasil/america-rn':'América-RN',
 'brasil/atletico':'Atlético-MG','brasil/atleticop':'Atlético-PR','brasil/botafogo-sp':'Botafogo-SP',
 'brasil/ceara':'Ceará','brasil/etti':'Etti Jundiaí','brasil/goias':'Goiás','brasil/gremio':'Grêmio',
 'brasil/internaciol-limeira':'Internacional de Limeira','brasil/marilia':'Marília','brasil/novohorizontino':'Novorizontino',
 'brasil/parana':'Paraná','brasil/pontepreta':'Ponte Preta','brasil/saocaetano':'São Caetano','brasil/saopaulo':'São Paulo',
 'brasil/selecaob':'Seleção Brasileira','brasil/selpaulista':'Seleção Paulista','brasil/vasco':'Vasco da Gama',
 'brasil/vitoria':'Vitória','brasil/xvpira':'XV de Piracicaba','italia/alzano-virescit':'Alzano Virescit',
 'italia/castel':'Castel di Sangro','italia/chievo':'Chievo Verona','italia/inter':'Internazionale','italia/italy':'Itália',
 'italia/provercelli':'Pro Vercelli','outros/america-mex':'Club América','outros/argentinos-jrs':'Argentinos Juniors',
 'outros/atletico-col':'Atlético Nacional','outros/austria':'Áustria','outros/barcelona-equ':'Barcelona (Equador)',
 'outros/bayern':'Bayern de Munique','outros/boca':'Boca Juniors','outros/bosnia':'Bósnia','outros/bulgaria':'Bulgária',
 'outros/cerro-uru':'Cerro (Uruguai)','outros/colombia':'Colômbia','outros/cruzazul':'Cruz Azul',
 'outros/cucuta':'Cúcuta Deportivo','outros/czechoslovakia':'Tchecoslováquia','outros/england':'Inglaterra',
 'outros/estudiantes':'Estudiantes','outros/france':'França','outros/germany':'Alemanha','outros/ghana':'Gana',
 'outros/japao':'Japão','outros/macedonia':'Macedônia','outros/manchester':'Manchester United',
 'outros/manchester-city':'Manchester City','outros/mexico':'México','outros/penarol':'Peñarol','outros/peru':'Peru',
 'outros/polonia':'Polônia','outros/qatar':'Catar','outros/queretaro':'Querétaro','outros/real':'Real Madrid',
 'outros/riverplate':'River Plate','outros/romania':'Romênia','outros/russia':'Rússia','outros/servia':'Sérvia',
 'outros/sovietunion':'União Soviética','outros/spain':'Espanha','outros/sportinglisboa':'Sporting CP',
 'outros/strongest':'The Strongest','outros/suecia':'Suécia','outros/switzerland':'Suíça','outros/turkey':'Turquia',
 'outros/universidad-chile':'Universidad de Chile','outros/uruguai':'Uruguai','outros/velez':'Vélez Sarsfield',
 'outros/vitoria-setubal-por':'Vitória de Setúbal','outros/widzew-lodz':'Widzew Łódź',
}

const lowerWords=new Set(['da','das','de','do','dos','e'])
const acronyms=new Map([['csa','CSA'],['spal','SPAL'],['xv','XV']])
const words=(value:string)=>value.trim().replaceAll('_',' ').replaceAll('-',' ').split(/\s+/).filter(Boolean)
const title=(value:string)=>words(value).map((word,index)=>{
 const lower=word.toLocaleLowerCase('pt-BR')
 if(acronyms.has(lower))return acronyms.get(lower)!
 if(index>0&&lowerWords.has(lower))return lower
 return lower.charAt(0).toLocaleUpperCase('pt-BR')+lower.slice(1)
}).join(' ')

export function teamDisplayName(identity:TeamIdentity|string,countrySlug?:string):string{
 const item=typeof identity==='string'?{slug:identity,name:identity,countrySlug}:identity
 const slug=(item.slug||item.name||'').trim().toLocaleLowerCase('pt-BR')
 const country=(item.countrySlug||countrySlug||'').trim().toLocaleLowerCase('pt-BR')
 return overrides[`${country}/${slug}`]||title(item.name||item.slug||'Equipe')
}

export const teamDisplayNameOverrides=overrides
