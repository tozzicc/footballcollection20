import NavigationItem from '../../components/navigation/NavigationItem'
import type { NavigationItem as NavigationItemType } from '../../types/navigation'

type SidebarProps = {
  items: NavigationItemType[]
  open: boolean
  onClose: () => void
}

const Sidebar = ({ items, open, onClose }: SidebarProps) => (
  <aside className={`sidebar ${open ? 'sidebar-open' : ''}`} aria-label="Navegação lateral" data-open={open}>
    <div className="sidebar-header">
      <div>
        <p className="sidebar-title">Navegação</p>
        <p className="sidebar-subtitle">Estrutura do app</p>
      </div>
      <button
        type="button"
        className="sidebar-close"
        aria-label="Fechar menu"
        onClick={onClose}
      >
        Fechar
      </button>
    </div>

    <nav className="sidebar-nav" aria-label="Links principais">
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <NavigationItem item={item} onNavigate={onClose} />
          </li>
        ))}
      </ul>
    </nav>
  </aside>
)

export default Sidebar
