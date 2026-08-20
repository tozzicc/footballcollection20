export const PAGE_SIZE=24

export const publicPageFrom=(value:string|null)=>{
 const page=Number(value)
 return Number.isInteger(page)&&page>0?page:1
}
