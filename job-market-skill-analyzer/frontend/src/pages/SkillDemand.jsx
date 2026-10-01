import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { getSkillDemand, getRoles, getLocations } from '../services/api.js'

export default function SkillDemand() {
  const [role, setRole] = useState('')
  const [location, setLocation] = useState('')
  const [roles, setRoles] = useState([])
  const [locations, setLocations] = useState([])
  const [demand, setDemand] = useState([])
  const [totalJobs, setTotalJobs] = useState(0)

  useEffect(() => {
    getRoles().then(setRoles)
    getLocations().then(setLocations)
  }, [])

  useEffect(() => {
    getSkillDemand({ role: role || undefined, location: location || undefined })
      .then(d => { setDemand(d.skills); setTotalJobs(d.total_jobs_considered) })
  }, [role, location])

  return (
    <div>
      <h2>Skill Demand</h2>
      <div className="card" style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="">All Roles</option>
          {roles.map(r => <option key={r} value={r}>{r}</option>)}
        </select>
        <select value={location} onChange={e => setLocation(e.target.value)}>
          <option value="">All Locations</option>
          {locations.map(l => <option key={l} value={l}>{l}</option>)}
        </select>
      </div>
      <p style={{ color: 'var(--color-muted)' }}>Based on {totalJobs} matching job postings.</p>

      <div className="card">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={demand} layout="vertical" margin={{ left: 80 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" unit="%" />
            <YAxis type="category" dataKey="skill" width={120} />
            <Tooltip formatter={v => `${v}%`} />
            <Bar dataKey="percentage" fill="#4f46e5" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
