const apiBase=(import.meta.env.VITE_API_BASE_URL??'').replace(/\/+$/,'')
export function resolveMediaUrl(value:string|null|undefined){
 if(!value)return null
 if(/^https?:\/\//i.test(value))return value
 return `${apiBase}/${value.replace(/^\/+/, '')}`
}
