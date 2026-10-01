import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, Search, TrendingUp, GitCompare, Network,
  Target, Map, LineChart, Settings,
} from 'lucide-react'

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/explorer', label: 'Job Explorer', icon: Search },
  { to: '/skill-demand', label: 'Skill Demand', icon: TrendingUp },
  { to: '/compare-roles', label: 'Compare Roles', icon: GitCompare },
  { to: '/skill-combinations', label: 'Skill Combinations', icon: Network },
  { to: '/skill-gap', label: 'My Skill Gap', icon: Target },
  { to: '/roadmap', label: 'Career Roadmap', icon: Map },
  { to: '/progress', label: 'My Progress', icon: LineChart },
]

export default function Sidebar() {
  return (
    <aside style={{
      width: 'var(--sidebar-width)', background: '#111827', color: '#fff',
      display: 'flex', flexDirection: 'column', padding: '20px 0', flexShrink: 0,
    }}>
      <div style={{ padding: '0 20px 20px', fontWeight: 700, fontSize: 16 }}>
        JOB MARKET<br />SKILL ANALYZER
      </div>
      <nav style={{ flex: 1 }}>
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} style={({ isActive }) => ({
            display: 'flex', alignItems: 'center', gap: 10,
            padding: '10px 20px', color: isActive ? '#fff' : '#9ca3af',
            background: isActive ? '#1f2937' : 'transparent',
            textDecoration: 'none', fontSize: 14,
          })}>
            <Icon size={18} /> {label}
          </NavLink>
        ))}
      </nav>
      <NavLink to="/settings" style={{
        display: 'flex', alignItems: 'center', gap: 10, padding: '10px 20px',
        color: '#9ca3af', textDecoration: 'none', fontSize: 14,
      }}>
        <Settings size={18} /> Settings
      </NavLink>
    </aside>
  )
}
