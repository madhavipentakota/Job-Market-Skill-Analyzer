import { useEffect, useState } from 'react'
import { Target, Plus } from 'lucide-react'
import { getRoles, analyzeSkillGap, saveUserSkills } from '../services/api.js'
import { useAuth } from '../context/AuthContext.jsx'

export default function SkillGap() {
  const [roles, setRoles] = useState([])
  const [targetRole, setTargetRole] = useState('')
  const [skillInput, setSkillInput] = useState('')
  const [currentSkills, setCurrentSkills] = useState([])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const { user, isAuthenticated } = useAuth()

  useEffect(() => { getRoles().then(setRoles) }, [])

  const addSkill = (text) => {
    const value = (text ?? skillInput).trim()
    if (!value) return currentSkills
    const updated = [...new Set([...currentSkills, value])]
    setCurrentSkills(updated)
    setSkillInput('')
    return updated
  }

  const removeSkill = (skill) => {
    setCurrentSkills(s => s.filter(x => x !== skill))
  }

  const analyze = async () => {
    if (!targetRole) return
    // BUG FIX: previously, text typed but not yet "Added" (no Enter / click)
    // was silently dropped, so it never reached the API and looked like the
    // skill was still "required". We flush any pending input here first.
    const finalSkills = skillInput.trim() ? addSkill() : currentSkills
    setLoading(true)
    try {
      const data = await analyzeSkillGap(targetRole, finalSkills)
      setResult(data)
      if (isAuthenticated) {
        saveUserSkills(user.user_id, finalSkills).catch(() => {})
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2><Target size={22} style={{ verticalAlign: 'text-bottom', marginRight: 6 }} />My Skill Gap</h2>

      <div className="card" style={{ marginBottom: 16 }}>
        <label style={{ fontWeight: 600, fontSize: 14 }}>Target Role</label><br />
        <select value={targetRole} onChange={e => { setTargetRole(e.target.value); setResult(null) }} style={{ marginTop: 6, minWidth: 240 }}>
          <option value="">Select a role</option>
          {roles.map(r => <option key={r} value={r}>{r}</option>)}
        </select>

        <div style={{ marginTop: 20 }}>
          <label style={{ fontWeight: 600, fontSize: 14 }}>Your Current Skills</label><br />
          <div style={{ display: 'flex', gap: 8, marginTop: 6 }}>
            <input
              value={skillInput}
              onChange={e => setSkillInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addSkill() } }}
              placeholder="e.g. Python — press Enter or click Add"
              style={{ flex: 1 }}
            />
            <button className="btn" onClick={() => addSkill()}><Plus size={16} /> Add</button>
          </div>
          <p style={{ fontSize: 12, color: 'var(--color-muted)', marginTop: 4 }}>
            Tip: click a badge below to remove it. Don't forget to click "Add" (or press Enter) —
            typed text left in the box won't count until it's added.
          </p>
          <div style={{ marginTop: 8, minHeight: 30 }}>
            {currentSkills.length === 0 && <span style={{ color: 'var(--color-muted)', fontSize: 13 }}>No skills added yet.</span>}
            {currentSkills.map(s => (
              <span key={s} className="skill-badge removable" onClick={() => removeSkill(s)} title="Click to remove">
                {s} ×
              </span>
            ))}
          </div>
        </div>

        <button className="btn" style={{ marginTop: 18 }} onClick={analyze} disabled={!targetRole || loading}>
          {loading ? 'Analyzing...' : 'Analyze Skill Gap'}
        </button>
        {!isAuthenticated && (
          <p style={{ fontSize: 12, color: 'var(--color-muted)', marginTop: 8 }}>
            Log in to save these skills and reuse them across the app.
          </p>
        )}
      </div>

      {result && (
        <div className="card">
          <h3>Skill Readiness: {result.readiness_percentage}%</h3>
          <div className="progress-bar-track">
            <div className="progress-bar-fill" style={{ width: `${result.readiness_percentage}%` }} />
          </div>
          <p style={{ fontSize: 12, color: 'var(--color-muted)' }}>
            This reflects coverage of skills found in this app's dataset for {result.target_role} — not a guarantee of employability.
          </p>

          <SkillList title="✓ Already Have" skills={result.already_have} color="#16a34a" />
          <SkillList title="⚠ Missing (High Priority)" skills={result.high_priority} color="#dc2626" />
          <SkillList title="⚠ Missing" skills={result.missing.filter(s => !result.high_priority.includes(s))} color="#f59e0b" />
          <SkillList title="Partially Covered / Nice-to-have" skills={result.partially_covered} color="#64748b" />
        </div>
      )}
    </div>
  )
}

function SkillList({ title, skills, color }) {
  if (!skills || skills.length === 0) return null
  return (
    <div style={{ marginTop: 12 }}>
      <b style={{ color }}>{title}</b>
      <div>{skills.map(s => <span key={s} className="skill-badge">{s}</span>)}</div>
    </div>
  )
}
