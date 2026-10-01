import { useState } from 'react'
import { NavLink, Link } from 'react-router-dom'
import {
  LayoutDashboard, Search, TrendingUp, GitCompare, Network,
  Target, Map, LineChart, Menu, X, LogOut, User as UserIcon,
} from 'lucide-react'
import { useAuth } from '../context/AuthContext.jsx'
import AuthModal from './AuthModal.jsx'

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/explorer', label: 'Job Explorer', icon: Search },
  { to: '/skill-demand', label: 'Skill Demand', icon: TrendingUp },
  { to: '/compare-roles', label: 'Compare Roles', icon: GitCompare },
  { to: '/skill-combinations', label: 'Skill Combos', icon: Network },
  { to: '/skill-gap', label: 'My Skill Gap', icon: Target },
  { to: '/roadmap', label: 'Career Roadmap', icon: Map },
  { to: '/progress', label: 'My Progress', icon: LineChart },
]

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [authMode, setAuthMode] = useState(null) // null | 'login' | 'signup'
  const { user, logout, isAuthenticated } = useAuth()

  return (
    <>
      <header className="navbar">
        <div className="navbar-inner">
          <Link to="/" className="navbar-brand" onClick={() => setMobileOpen(false)}>
            Job Market <span>Skill Analyzer</span>
          </Link>

          <nav className={`navbar-links ${mobileOpen ? 'open' : ''}`}>
            {links.map(({ to, label, icon: Icon }) => (
              <NavLink key={to} to={to} className={({ isActive }) => isActive ? 'active' : ''}
                onClick={() => setMobileOpen(false)}>
                <Icon size={16} /> {label}
              </NavLink>
            ))}
          </nav>

          <div className="navbar-actions">
            {isAuthenticated ? (
              <div className="navbar-user">
                <span><UserIcon size={16} /> {user.full_name || user.email}</span>
                <button className="btn-ghost" onClick={logout}><LogOut size={15} /> Log out</button>
              </div>
            ) : (
              <>
                <button className="btn-ghost" onClick={() => setAuthMode('login')}>Log In</button>
                <button className="btn" onClick={() => setAuthMode('signup')}>Sign Up</button>
              </>
            )}
            <button className="navbar-burger" onClick={() => setMobileOpen(o => !o)} aria-label="Menu">
              {mobileOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>
      </header>

      {authMode && <AuthModal mode={authMode} onClose={() => setAuthMode(null)} />}
    </>
  )
}
