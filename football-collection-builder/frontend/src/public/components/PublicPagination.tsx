import { PAGE_SIZE } from '../utils/publicPagination'

export default function PublicPagination({page,total,onChange}:{page:number;total:number;onChange:(page:number)=>void}){
 const pages=Math.max(1,Math.ceil(total/PAGE_SIZE)),safePage=Math.min(page,pages)
 if(pages<=1)return null
 const first=(safePage-1)*PAGE_SIZE+1,last=Math.min(safePage*PAGE_SIZE,total)
 return <nav className="public-pagination" aria-label="Paginação de equipes">
  <button disabled={safePage===1} onClick={()=>onChange(safePage-1)}>Anterior</button>
  <span><strong>Página {safePage} de {pages}</strong><small>{first}–{last} de {total} equipes</small></span>
  <button disabled={safePage===pages} onClick={()=>onChange(safePage+1)}>Próxima</button>
 </nav>
}
