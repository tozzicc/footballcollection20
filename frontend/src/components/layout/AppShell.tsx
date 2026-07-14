import { useState, useEffect } from 'react'
import Sidebar from './Sidebar'
import Topbar from './Topbar'
import MainContent from './MainContent'
import Footer from './Footer'
import navigation from '../../data/navigation'

const AppShell = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const handleToggleSidebar = () => setSidebarOpen((current) => !current)
  const handleCloseSidebar = () => setSidebarOpen(false)

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setSidebarOpen(false)
      }
    }

    if (sidebarOpen) {
      document.body.style.overflow = 'hidden'
      window.addEventListener('keydown', onKey)
    } else {
      document.body.style.overflow = ''
    }

    return () => {
      window.removeEventListener('keydown', onKey)
      document.body.style.overflow = ''
    }
  }, [sidebarOpen])

  return (
    <div className={`app-shell${sidebarOpen ? ' shell-sidebar-open' : ''}`}>
      <Topbar onToggleSidebar={handleToggleSidebar} />

      {sidebarOpen && (
        <div className="sidebar-backdrop" aria-hidden="true" onClick={handleCloseSidebar} />
      )}

      <div className="shell-layout">
        <Sidebar items={navigation} open={sidebarOpen} onClose={handleCloseSidebar} />

        <div className="shell-main">
          <MainContent />
          <Footer />
        </div>
      </div>
    </div>
  )
}

export default AppShell
