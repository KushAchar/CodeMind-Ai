import {
  Bot,
  BrainCircuit,
  ChevronDown,
  FolderGit2,
  LayoutDashboard,
  Network,
  Settings,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'
import Logo from './Logo'

const navigation = [
  { label: 'Dashboard', icon: LayoutDashboard, to: '/' },
  { label: 'Repositories', icon: FolderGit2, to: '/repositories' },
  { label: 'AI Assistant', icon: Bot, to: '/assistant' },
  { label: 'Code Analysis', icon: Network, to: '/analysis' },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <Logo />
      <div className="workspace-switcher">
        <div className="workspace-avatar">K</div>
        <div>
          <span className="workspace-label">Workspace</span>
          <strong>Personal workspace</strong>
        </div>
        <ChevronDown size={16} className="muted-icon" />
      </div>

      <nav className="sidebar-nav" aria-label="Main navigation">
        <p className="nav-section-label">Overview</p>
        {navigation.map(({ label, icon: Icon, to }) => (
          <NavLink
            key={label}
            to={to}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <Icon size={18} />
            <span>{label}</span>
            {label === 'Repositories' && <span className="nav-count">12</span>}
          </NavLink>
        ))}
        <p className="nav-section-label">Workspace</p>
        <NavLink to="/settings" className="nav-item">
          <Settings size={18} />
          <span>Settings</span>
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <div className="pro-card">
          <div className="pro-icon"><BrainCircuit size={17} /></div>
          <div>
            <strong>Unlock more insights</strong>
            <span>Explore CodeMind Pro</span>
          </div>
        </div>
        <div className="profile">
          <div className="profile-avatar">KA</div>
          <div>
            <strong>Khush Achar</strong>
            <span>Developer</span>
          </div>
          <ChevronDown size={16} className="muted-icon" />
        </div>
      </div>
    </aside>
  )
}
