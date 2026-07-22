import { useCallback, useEffect, useState } from 'react'
import {
  getHtmlPage, getHtmlPages, getHtmlParserStatus, getMissingReferences, parseHtml,
} from '../services/htmlParserService'
import type {
  HtmlPageDetails, HtmlPagesResponse, HtmlParserStatus, MissingReferencesResponse,
} from '../types/htmlParser'

const emptyPages: HtmlPagesResponse = { items: [], total: 0, limit: 50, offset: 0 }
const emptyMissing: MissingReferencesResponse = { items: [], total: 0, limit: 50, offset: 0 }

const useHtmlParser = (workspacePath: string) => {
  const [status, setStatus] = useState<HtmlParserStatus | null>(null)
  const [pages, setPages] = useState(emptyPages)
  const [missing, setMissing] = useState(emptyMissing)
  const [details, setDetails] = useState<HtmlPageDetails | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isParsing, setIsParsing] = useState(false)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')
  const [pageOffset, setPageOffset] = useState(0)
  const [missingOffset, setMissingOffset] = useState(0)

  const refresh = useCallback(async () => {
    setIsLoading(true); setError('')
    try {
      const current = await getHtmlParserStatus()
      setStatus(current)
      if (current.hasRun) {
        const [pageData, missingData] = await Promise.all([
          getHtmlPages(50, pageOffset, search), getMissingReferences(50, missingOffset),
        ])
        setPages(pageData); setMissing(missingData)
      } else {
        setPages(emptyPages); setMissing(emptyMissing)
      }
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Falha ao consultar o Parser HTML.')
    } finally { setIsLoading(false) }
  }, [missingOffset, pageOffset, search])

  useEffect(() => {
    const timer = window.setTimeout(() => { void refresh() }, 0)
    return () => window.clearTimeout(timer)
  }, [refresh])
  const run = useCallback(async () => {
    setIsParsing(true); setError('')
    try { await parseHtml(workspacePath); setPageOffset(0); setMissingOffset(0); await refresh() }
    catch (caught) { setError(caught instanceof Error ? caught.message : 'Falha ao executar o parser.') }
    finally { setIsParsing(false) }
  }, [refresh, workspacePath])
  const openDetails = useCallback(async (id: number) => {
    try { setDetails(await getHtmlPage(id)) }
    catch (caught) { setError(caught instanceof Error ? caught.message : 'Falha ao abrir detalhes.') }
  }, [])
  return {
    status, pages, missing, details, isLoading, isParsing, error, search, pageOffset,
    missingOffset, setSearch, setPageOffset, setMissingOffset, setDetails, refresh, run, openDetails,
  }
}
export default useHtmlParser
