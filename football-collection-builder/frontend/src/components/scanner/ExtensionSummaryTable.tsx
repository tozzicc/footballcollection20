import type { ScannerResponse } from '../../types/scanner'

type ExtensionSummaryTableProps = {
  result: ScannerResponse
}

const ExtensionSummaryTable = ({ result }: ExtensionSummaryTableProps) => {
  const totalFiles = result.totalFiles || 1

  return (
    <div className="card-surface scanner-table-wrapper">
      <h3 className="scanner-table-title">Extensões encontradas</h3>
      <table className="scanner-table">
        <thead>
          <tr>
            <th className="scanner-table-head">Extensão</th>
            <th className="scanner-table-head">Quantidade</th>
            <th className="scanner-table-head">Percentual</th>
          </tr>
        </thead>
        <tbody>
          {result.extensions.map((item) => (
            <tr key={item.extension}>
              <td className="scanner-table-cell">{item.extension || '(sem extensão)'}</td>
              <td className="scanner-table-cell">{item.count}</td>
              <td className="scanner-table-cell">{((item.count / totalFiles) * 100).toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default ExtensionSummaryTable
