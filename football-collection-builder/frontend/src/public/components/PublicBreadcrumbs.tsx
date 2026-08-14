import { Link } from 'react-router-dom'
export interface PublicBreadcrumb {label:string;to?:string}
export default function PublicBreadcrumbs({items}:{items:PublicBreadcrumb[]}){return <nav className="public-breadcrumbs" aria-label="Breadcrumb"><ol><li><Link to="/site">Início</Link></li>{items.map((x,i)=><li key={`${x.label}-${i}`}>{x.to?<Link to={x.to}>{x.label}</Link>:<span aria-current="page">{x.label}</span>}</li>)}</ol></nav>}
