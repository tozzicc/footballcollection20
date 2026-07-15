import { useCallback, useState } from 'react'
import type { ScannerResponse, ScannerStatus } from '../types/scanner'
import { scanWorkspace } from '../services/scannerService'

export const useScanner = () => {
  const [scanResult, setScanResult] = useState<ScannerResponse | null>(null)
  const [isScanning, setIsScanning] = useState(false)
  const [scanError, setScanError] = useState<string>('')
  const [status, setStatus] = useState<ScannerStatus>('idle')

  const resetScan = useCallback(() => {
    setScanResult(null)
    setScanError('')
    setStatus('idle')
  }, [])

  const runScan = useCallback(async (workspacePath: string) => {
    if (isScanning) {
      return
    }

    setIsScanning(true)
    setScanError('')
    setStatus('scanning')

    try {
      const result = await scanWorkspace(workspacePath)
      setScanResult(result)
      setStatus('completed')
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Falha inesperada ao analisar o acervo.'
      setScanError(message)
      setStatus('error')
    } finally {
      setIsScanning(false)
    }
  }, [isScanning])

  return {
    runScan,
    scanResult,
    isScanning,
    scanError,
    resetScan,
    status,
  }
}
