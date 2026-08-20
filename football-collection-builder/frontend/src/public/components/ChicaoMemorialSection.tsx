import { Link } from 'react-router-dom'

export default function ChicaoMemorialSection(){
 return <section className="public-section public-chicao-memorial" aria-labelledby="chicao-memorial-title">
  <h2 id="chicao-memorial-title" className="sr-only">Chicão — O Deus da Raça</h2>
  <img src="/assets/collections/chicao-memorial-home.png" alt="Homenagem a Chicão — O Deus da Raça" loading="lazy"/>
  <Link className="public-chicao-memorial-link" to="/site/chicao" aria-label="Conhecer a história de Chicão"/>
 </section>
}
