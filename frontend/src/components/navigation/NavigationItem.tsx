import { NavLink } from 'react-router-dom'
import type { NavigationItem as NavigationItemType } from '../../types/navigation'

type NavigationItemProps = {
  item: NavigationItemType
  onNavigate?: () => void
}

const NavigationItem = ({ item, onNavigate }: NavigationItemProps) => {
  return (
    <NavLink
      to={item.path}
      className={({ isActive }: { isActive: boolean }) => (isActive ? 'nav-link nav-link-active' : 'nav-link')}
      onClick={() => onNavigate && onNavigate()}
    >
      <span>{item.label}</span>
    </NavLink>
  )
}

export default NavigationItem
