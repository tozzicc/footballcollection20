const DEFAULT_TIMEOUT_MS = 10000

export type ApiClientOptions = {
  baseUrl?: string
  timeoutMs?: number
}

export class ApiClient {
  private baseUrl: string
  private timeoutMs: number

  constructor(options: ApiClientOptions = {}) {
    this.baseUrl = options.baseUrl ?? import.meta.env.VITE_API_BASE_URL ?? ''
    this.timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS
  }

  private buildUrl(path: string): string {
    return `${this.baseUrl.replace(/\/+$/, '')}/${path.replace(/^\/+/, '')}`
  }

  private async parseJson(response: Response) {
    const text = await response.text()
    if (!text) {
      return null
    }

    try {
      return JSON.parse(text)
    } catch {
      throw new Error('Resposta inválida do servidor.')
    }
  }

  async post<T>(path: string, body: unknown): Promise<T> {
    const controller = new AbortController()
    const timeout = window.setTimeout(() => controller.abort(), this.timeoutMs)

    try {
      const response = await fetch(this.buildUrl(path), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      })

      if (!response.ok) {
        const payload = await this.parseJson(response).catch(() => null)
        const message = payload?.detail ?? `Erro HTTP ${response.status}`
        throw new Error(message)
      }

      return await this.parseJson(response)
    } catch (caughtError: unknown) {
      if (caughtError instanceof DOMException && caughtError.name === 'AbortError') {
        throw new Error('Tempo de conexão excedido com o backend.', {
          cause: caughtError,
        })
      }
      if (caughtError instanceof Error) {
        throw caughtError
      }

      throw new Error('Erro na requisição ao backend.', {
        cause: caughtError,
      })
    } finally {
      window.clearTimeout(timeout)
    }
  }
}
