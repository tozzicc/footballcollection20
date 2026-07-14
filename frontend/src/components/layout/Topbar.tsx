type TopbarProps = {
  onToggleSidebar: () => void
}

const Topbar = ({ onToggleSidebar }: TopbarProps) => (
  <header className="topbar" aria-label="Barra superior">
    <div className="topbar-brand">
      <div>
        <p className="topbar-eyebrow">Football Collection Builder</p>
        <strong className="topbar-title">Museum Edition</strong>
      </div>
    </div>

    <div className="topbar-actions">
      <span className="topbar-version">v0.1.0-alpha</span>
      <button
        type="button"
        className="topbar-menu-button"
        aria-label="Abrir menu de navegação"
        onClick={onToggleSidebar}
      >
        Menu
      </button>
    </div>
  </header>
)

export default Topbar
