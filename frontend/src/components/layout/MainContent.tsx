import { Outlet } from 'react-router-dom'

const MainContent = () => (
  <main className="main-content" aria-label="Conteúdo principal">
    <Outlet />
  </main>
)

export default MainContent
