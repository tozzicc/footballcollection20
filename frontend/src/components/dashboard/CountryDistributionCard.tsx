import ProgressBar from '../ui/ProgressBar'
import type { CountrySummary } from '../../types/dashboard'

type CountryDistributionCardProps = {
  countries: CountrySummary[]
}

const CountryDistributionCard = ({ countries }: CountryDistributionCardProps) => {
  const total = countries.reduce((sum, c) => sum + c.count, 0)

  return (
    <div className="distribution-container">
      <div className="distribution-list">
        {countries.map((country) => (
          <div key={country.id} className="distribution-item">
            <div className="distribution-header">
              <h3 className="distribution-name">{country.name}</h3>
              <span className="distribution-count">{country.count.toLocaleString('pt-BR')}</span>
            </div>
            <ProgressBar
              value={country.count}
              max={total}
              showPercentage
              ariaLabel={`Distribuição em ${country.name}`}
            />
          </div>
        ))}
      </div>
    </div>
  )
}

export default CountryDistributionCard
