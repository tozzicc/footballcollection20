import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AppShell from '../components/layout/AppShell'
import DashboardPage from '../pages/DashboardPage'
import WorkspacePage from '../pages/WorkspacePage'
import ScannerPage from '../pages/ScannerPage'
import InventoryPage from '../pages/InventoryPage'
import HtmlParserPage from '../pages/HtmlParserPage'
import ImageParserPage from '../pages/ImageParserPage'
import CatalogPage from '../pages/CatalogPage'
import CatalogQualityPage from '../pages/CatalogQualityPage'
import CatalogReviewPage from '../pages/CatalogReviewPage'
import CatalogNormalizationPage from '../pages/CatalogNormalizationPage'
import PublicCatalogModelPage from '../pages/PublicCatalogModelPage'
import MediaLayerPage from '../pages/MediaLayerPage'
import ReportsPage from '../pages/ReportsPage'
import ExportsPage from '../pages/ExportsPage'
import LogsPage from '../pages/LogsPage'
import SettingsPage from '../pages/SettingsPage'
import NotFoundPage from '../pages/NotFoundPage'
import PublicLayout from '../public/layout/PublicLayout'
import { PublicCountriesPage, PublicCountryPage, PublicNotFoundPage, PublicSearchPage, PublicTeamsPage } from '../public/pages/PublicPages'
import { PublicCollectionEditorialPage, PublicHomeEditorialPage, PublicItemEditorialPage, PublicLatestEditorialPage, PublicTeamEditorialPage } from '../public/pages/PublicEditorialPages'

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/site" element={<PublicLayout />}>
        <Route index element={<PublicHomeEditorialPage />} />
        <Route path="paises" element={<PublicCountriesPage />} />
        <Route path="paises/:countrySlug" element={<PublicCountryPage />} />
        <Route path="equipes" element={<PublicTeamsPage />} />
        <Route path="paises/:countrySlug/equipes/:teamSlug" element={<PublicTeamEditorialPage />} />
        <Route path="paises/:countrySlug/equipes/:teamSlug/collections/:collectionSlug" element={<PublicCollectionEditorialPage />} />
        <Route path="items/:countrySlug/teams/:teamSlug/collections/:collectionSlug/:itemSlug" element={<PublicItemEditorialPage />} />
        <Route path="items/:countrySlug/teams/:teamSlug/items/:itemSlug" element={<PublicItemEditorialPage />} />
        <Route path="busca" element={<PublicSearchPage />} />
        <Route path="ultimas" element={<PublicLatestEditorialPage />} />
        <Route path="*" element={<PublicNotFoundPage />} />
      </Route>
      <Route path="/" element={<AppShell />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="workspace" element={<WorkspacePage />} />
        <Route path="scanner" element={<ScannerPage />} />
        <Route path="inventory" element={<InventoryPage />} />
        <Route path="parser-html" element={<HtmlParserPage />} />
        <Route path="parser-imagens" element={<ImageParserPage />} />
        <Route path="catalogo" element={<CatalogPage />} />
        <Route path="qualidade-catalogo" element={<CatalogQualityPage />} />
        <Route path="revisao-catalogo" element={<CatalogReviewPage />} />
        <Route path="normalizacao-catalogo" element={<CatalogNormalizationPage />} />
        <Route path="modelo-publico" element={<PublicCatalogModelPage />} />
        <Route path="midia-site" element={<MediaLayerPage />} />
        <Route path="relatorios" element={<ReportsPage />} />
        <Route path="exportacoes" element={<ExportsPage />} />
        <Route path="logs" element={<LogsPage />} />
        <Route path="configuracoes" element={<SettingsPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  </BrowserRouter>
)

export default AppRouter
