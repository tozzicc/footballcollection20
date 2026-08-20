export interface PublicHeroMediaConfig {
  src: string
  alt: string
  width: number
  height: number
}

export const publicSiteConfig: { heroMedia: PublicHeroMediaConfig } = {
  heroMedia: {
    src: '/assets/collections/football-collection-hero-v2.png',
    alt: 'Composição editorial do acervo histórico Football Collection',
    width: 1774,
    height: 887,
  },
}
