import { useEffect, useState } from 'react'
import { getJobs, getRoles, getLocations } from '../services/api.js'

export default function JobExplorer() {
  const [jobs, setJobs] = useState([])
  const [roles, setRoles] = useState([])
  const [locations, setLocations] = useState([])
  const [filters, setFilters] = useState({ role: '', location: '', search: '' })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getRoles().then(setRoles)
    getLocations().then(setLocations)
  }, [])

  useEffect(() => {
    setLoading(true)
    getJobs(filters).then(setJobs).finally(() => setLoading(false))
  }, [filters])

  return (
    <div>
      <h2>Job Market Explorer</h2>
      <div className="card" style={{ display: 'flex', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
        <input placeholder="Search job title..." value={filters.search}
          onChange={e => setFilters(f => ({ ...f, search: e.target.value }))} />
        <select value={filters.role} onChange={e => setFilters(f => ({ ...f, role: e.target.value }))}>
          <option value="">All Roles</option>
          {roles.map(r => <option key={r} value={r}>{r}</option>)}
        </select>
        <select value={filters.location} onChange={e => setFilters(f => ({ ...f, location: e.target.value }))}>
          <option value="">All Locations</option>
          {locations.map(l => <option key={l} value={l}>{l}</option>)}
        </select>
      </div>

      {loading ? <p>Loading jobs...</p> : jobs.length === 0 ? <p>No jobs match these filters.</p> : (
        <div style={{ display: 'grid', gap: 12 }}>
          {jobs.map(job => (
            <div key={job.id} className="card">
              <h4 style={{ margin: 0 }}>{job.job_title} — {job.company}</h4>
              <p style={{ margin: '4px 0', color: 'var(--color-muted)' }}>
                {job.location} · {job.experience} · {job.salary}
              </p>
              <div>{job.skills.map(s => <span key={s} className="skill-badge">{s}</span>)}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
