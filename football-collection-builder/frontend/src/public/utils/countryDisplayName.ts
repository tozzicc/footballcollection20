const countryNames:Record<string,string>={brasil:'Brasil',italia:'Itália',outros:'Outros'}

export function countryDisplayName(value:string|null|undefined):string{
 const raw=(value||'').trim()
 const key=raw.toLocaleLowerCase('pt-BR')
 return countryNames[key]||(raw?raw.charAt(0).toLocaleUpperCase('pt-BR')+raw.slice(1):'')
}

export const countryDisplayNames=countryNames
