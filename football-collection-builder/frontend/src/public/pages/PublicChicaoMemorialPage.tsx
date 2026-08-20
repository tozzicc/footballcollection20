import { Link } from 'react-router-dom'
import PublicBreadcrumbs from '../components/PublicBreadcrumbs'
import { usePageTitle } from '../hooks/usePublicData'

const memoryImages=[
 {src:'/assets/chicao/sao-paulo.jpg',alt:'Imagem histórica identificada no memorial como São Paulo',label:'São Paulo',to:'/site/chicao/camisas/sao-paulo'},
 {src:'/assets/chicao/selecao-brasileira.jpg',alt:'Imagem histórica identificada no memorial como Seleção Brasileira',label:'Seleção Brasileira',to:'/site/chicao/camisas/selecao-brasileira'},
 {src:'/assets/chicao/santos.jpg',alt:'Imagem histórica identificada no memorial como Santos',label:'Santos'},
 {src:'/assets/chicao/atletico-mineiro.jpg',alt:'Imagem histórica identificada no memorial como Atlético Mineiro',label:'Atlético-MG',to:'/site/chicao/camisas/atletico-mg'},
]

const memorialVideos=[
 {src:'/assets/chicao/videos/brasileiro-1977.mp4',title:'Brasileiro 1977'},
 {src:'/assets/chicao/videos/entrevista-2005.mp4',title:'Entrevista em 2005'},
 {src:'/assets/chicao/videos/sao-paulo-3x2-santos-1981-chicao-perde-o-bigode.mp4',title:'São Paulo 3×2 Santos — 1981 — Chicão perde o bigode'},
]

export default function PublicChicaoMemorialPage(){
 usePageTitle('Chicão — O Deus da Raça')
 return <article className="public-memorial-page">
  <PublicBreadcrumbs items={[{label:'Chicão — O Deus da Raça'}]}/>
  <header className="public-memorial-header">
   <div>
    <p className="public-kicker">Homenagem</p>
    <h1>Chicão</h1>
    <p className="public-memorial-subtitle">O Deus da Raça</p>
   </div>
   <figure className="public-memorial-opening">
    <img src="/assets/chicao/memorial-entry.jpg" alt="Imagem histórica utilizada na entrada original da homenagem a Chicão"/>
   </figure>
  </header>

  <section className="public-memorial-testimony" aria-labelledby="memorial-testimony-title">
   <p className="public-kicker">Memória preservada</p>
   <h2 id="memorial-testimony-title">Uma homenagem a Chicão</h2>
   <blockquote>
    <p>Sem dúvida foi um Amigo em pouco tempo, um rapaz simples, um Homem seguro em campo e ao mesmo tempo, um menino humilde fora dele, valorizava a minha pessoa mais do que devia, para ele talvez a nossa amizade era bem mais do que uma simples Amizade, me fez sentir um irmão e me tratou as vezes como filho.</p>
    <p>Posso afirmar que tenho muito orgulho em ter conhecido este menino maravilhoso com um coração enorme, este homem humilde e carinhoso com todas as pessoas que tiveram oportunidade de conhecê-lo .</p>
    <p>Lembro me como se fosse hoje a primeira vez em que o conheci em 1988, fiquei muito impressionado quanto a bondade e humildade dele, e sem dúvida, foi com esta mesma humildade e bondade, que ele se apresentou a DEUS.</p>
    <footer>— Mauro Matta</footer>
   </blockquote>
  </section>

  <section className="public-memorial-section" aria-labelledby="memorial-images-title">
   <div className="public-section-heading"><h2 id="memorial-images-title">Memória em imagens</h2></div>
   <div className="public-memorial-gallery">
    {memoryImages.map(image=>{
     const card=<figure><img src={image.src} alt={image.alt} loading="lazy"/><figcaption>{image.label}</figcaption></figure>
     return image.to?<Link className="public-memorial-gallery-link" key={image.src} to={image.to} aria-label={`Ver item do acervo relacionado a ${image.label}`}>{card}</Link>:<div className="public-memorial-gallery-static" key={image.src}>{card}</div>
    })}
   </div>
  </section>

  <section className="public-memorial-audiovisual" aria-labelledby="memorial-video-title">
   <p className="public-kicker">Acervo preservado</p>
   <h2 id="memorial-video-title">Registro audiovisual</h2>
   <div className="public-memorial-video-grid">
    {memorialVideos.map(video=><article className="public-memorial-video" key={video.src}><video controls preload="metadata"><source src={video.src} type="video/mp4"/>Seu navegador não oferece suporte à reprodução deste vídeo.</video><h3>{video.title}</h3></article>)}
   </div>
  </section>
 </article>
}
