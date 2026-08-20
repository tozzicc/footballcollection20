import type { HistoricalSectionKey } from '../../types/historicalCollections'

type EditorialCover = { src: string; alt: string }

export const historicalSectionCovers: Record<HistoricalSectionKey, EditorialCover> = {
  pennants: { src: '/assets/collections/colecoes-flamulas-v2.jpg', alt: 'Composição visual de flâmulas históricas de futebol' },
  flags: { src: '/assets/collections/colecoes-bandeiras-v2.jpg', alt: 'Composição visual de bandeiras históricas de futebol' },
  memorabilia: { src: '/assets/collections/colecoes-memorabilia-v2.jpg', alt: 'Composição visual de memorabilia de futebol' },
}

export const pennantGroupCovers: Record<string, EditorialCover> = {
  brasil: { src: '/assets/collections/flamulas-brasil-v2.jpg', alt: 'Composição visual representando flâmulas do Brasil' },
  italy: { src: '/assets/collections/flamulas-italia-v2.jpg', alt: 'Composição visual representando flâmulas da Itália' },
  other: { src: '/assets/collections/flamulas-outros-v2.jpg', alt: 'Composição visual representando flâmulas internacionais' },
}
