import { useEffect, useState } from 'react'
import { getSkillCombinations } from '../services/api.js'

export default function SkillCombinations() {
  const [pairs, setPairs] = useState([])

  useEffect(() => { getSkillCombinations(15).then(d => setPairs(d.pairs)) }, [])

  return (
    <div>
      <h2>Skill Combinations</h2>
      <p style={{ color: 'var(--color-muted)' }}>Skills that frequently appear together in the same job posting.</p>
      <div style={{ display: 'grid', gap: 10 }}>
        {pairs.map((p, i) => (
          <div key={i} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span className="skill-badge">{p.skills[0]}</span> + <span className="skill-badge">{p.skills[1]}</span>
            </div>
            <div style={{ color: 'var(--color-muted)' }}>{p.count} jobs · {p.percentage}%</div>
          </div>
        ))}
      </div>
    </div>
  )
}
