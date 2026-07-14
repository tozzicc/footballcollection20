import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AppShell from '../components/layout/AppShell'
import DashboardPage from '../pages/DashboardPage'
import WorkspacePage from '../pages/WorkspacePage'
import ScannerPage from '../pages/ScannerPage'
import CatalogPage from '../pages/CatalogPage'
import ReportsPage from '../pages/ReportsPage'
import ExportsPage from '../pages/ExportsPage'
import LogsPage from '../pages/LogsPage'
import SettingsPage from '../pages/SettingsPage'
import NotFoundPage from '../pages/NotFoundPage'

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<AppShell />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="workspace" element={<WorkspacePage />} />
        <Route path="scanner" element={<ScannerPage />} />
        <Route path="catalogo" element={<CatalogPage />} />
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
