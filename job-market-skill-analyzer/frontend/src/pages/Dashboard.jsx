import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { getJobs, getSkillDemand } from '../services/api.js'

export default function Dashboard() {
  const [jobs, setJobs] = useState([])
  const [demand, setDemand] = useState([])

  useEffect(() => {
    getJobs().then(setJobs).catch(() => {})
    getSkillDemand().then(d => setDemand(d.skills.slice(0, 10))).catch(() => {})
  }, [])

  const topSkill = demand[0]?.skill || '—'
  const roleCounts = jobs.reduce((acc, j) => {
    acc[j.job_title] = (acc[j.job_title] || 0) + 1
    return acc
  }, {})
  const topRole = Object.entries(roleCounts).sort((a, b) => b[1] - a[1])[0]?.[0] || '—'
  const locations = [...new Set(jobs.map(j => j.location))].slice(0, 5)

  return (
    <div>
      <h2>Dashboard</h2>
      <p style={{ color: 'var(--color-muted)', fontSize: 13 }}>
        Demo dataset — {jobs.length} sample job postings.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, margin: '16px 0' }}>
        <div className="card"><b>{jobs.length}</b><div>Jobs Analyzed</div></div>
        <div className="card"><b>{demand.length}</b><div>Top Skills Tracked</div></div>
        <div className="card"><b>{topSkill}</b><div>Most Demanded Skill</div></div>
        <div className="card"><b>{topRole}</b><div>Most Popular Role</div></div>
      </div>

      <div className="card">
        <h3>Top 10 Skills</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={demand}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="skill" angle={-30} textAnchor="end" interval={0} height={70} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="percentage" fill="#4f46e5" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <h3>Top Locations</h3>
        {locations.map(l => <span key={l} className="skill-badge">{l}</span>)}
      </div>
    </div>
  )
}
