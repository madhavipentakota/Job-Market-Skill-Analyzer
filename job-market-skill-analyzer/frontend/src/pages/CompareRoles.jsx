import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from 'recharts'
import { getRoles, compareRoles } from '../services/api.js'

export default function CompareRoles() {
  const [roles, setRoles] = useState([])
  const [roleA, setRoleA] = useState('')
  const [roleB, setRoleB] = useState('')
  const [chartData, setChartData] = useState([])

  useEffect(() => { getRoles().then(setRoles) }, [])

  useEffect(() => {
    if (!roleA || !roleB) return
    compareRoles([roleA, roleB]).then(result => {
      const skillsA = result[roleA] || []
      const skillsB = result[roleB] || []
      const allSkills = [...new Set([...skillsA.map(s => s.skill), ...skillsB.map(s => s.skill)])]
      const merged = allSkills.map(skill => ({
        skill,
        [roleA]: skillsA.find(s => s.skill === skill)?.percentage || 0,
        [roleB]: skillsB.find(s => s.skill === skill)?.percentage || 0,
      }))
      setChartData(merged)
    })
  }, [roleA, roleB])

  return (
    <div>
      <h2>Compare Roles</h2>
      <div className="card" style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
        <select value={roleA} onChange={e => setRoleA(e.target.value)}>
          <option value="">Select Role A</option>
          {roles.map(r => <option key={r} value={r}>{r}</option>)}
        </select>
        <select value={roleB} onChange={e => setRoleB(e.target.value)}>
          <option value="">Select Role B</option>
          {roles.map(r => <option key={r} value={r}>{r}</option>)}
        </select>
      </div>

      {chartData.length > 0 && (
        <div className="card">
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="skill" angle={-30} textAnchor="end" interval={0} height={80} />
              <YAxis unit="%" />
              <Tooltip formatter={v => `${v}%`} />
              <Legend />
              <Bar dataKey={roleA} fill="#4f46e5" />
              <Bar dataKey={roleB} fill="#f59e0b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
