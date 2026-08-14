export const PublicLoading=()=> <div className="public-state" role="status"><span className="public-loader"/>Carregando acervo...</div>
export const PublicError=()=> <div className="public-state"><h2>Não foi possível carregar este conteúdo.</h2><p>Tente novamente em alguns instantes.</p></div>
export const PublicEmpty=({message='Nenhum conteúdo encontrado.'}:{message?:string})=> <div className="public-state"><h2>{message}</h2><p>Explore outra área da coleção.</p></div>
