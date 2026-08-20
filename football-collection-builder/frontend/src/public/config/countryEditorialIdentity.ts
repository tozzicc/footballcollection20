export interface CountryEditorialCover {
  src: string
  alt: string
}

export const countryEditorialCovers: Record<string, CountryEditorialCover> = {
  brasil: {
    src: '/assets/collections/paises-brasil.png',
    alt: 'Acervo de camisas do futebol brasileiro',
  },
  italia: {
    src: '/assets/collections/paises-italia.png',
    alt: 'Acervo de camisas do futebol italiano',
  },
  outros: {
    src: '/assets/collections/paises-outros.png',
    alt: 'Acervo internacional de camisas de futebol',
  },
}
