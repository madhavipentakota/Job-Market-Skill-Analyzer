import { useEffect, useState } from 'react'
import { Map, CheckCircle2 } from 'lucide-react'
import { getRoadmaps, getUserProgress, updateUserProgress } from '../services/api.js'
import { useAuth } from '../context/AuthContext.jsx'

const ACTIVE_ROADMAP_KEY = 'jmsa_active_roadmap'

export default function CareerRoadmap() {
  const [roadmaps, setRoadmaps] = useState([])
  const [selected, setSelected] = useState(null)
  const [activeStage, setActiveStage] = useState(null)
  const [stageStatus, setStageStatus] = useState({}) // { stage_id: 'completed' | 'not_started' | ... }
  const { user, isAuthenticated } = useAuth()

  useEffect(() => { getRoadmaps().then(setRoadmaps) }, [])

  const openRoadmap = async (roadmap) => {
    setSelected(roadmap)
    setActiveStage(null)
    localStorage.setItem(ACTIVE_ROADMAP_KEY, roadmap.role_name)

    // BUG FIX: previously progress was only kept in local component state and
    // reset to empty every time this page loaded, and the percentage was
    // computed against however many stages had EVER been touched (often
    // just 1), so checking a single box looked like "100%". We now always
    // fetch the real per-stage status from the backend, scoped to this
    // roadmap's full stage count.
    if (isAuthenticated) {
      const progress = await getUserProgress(user.user_id, roadmap.role_name)
      const statusMap = {}
      progress.stages.forEach(s => { statusMap[s.stage_id] = s.status })
      setStageStatus(statusMap)
    } else {
      setStageStatus({})
    }
  }

  const toggleComplete = (stageId) => {
    if (!isAuthenticated) {
      alert('Please log in to save your progress.')
      return
    }
    const isCurrentlyDone = stageStatus[stageId] === 'completed'
    const newStatus = isCurrentlyDone ? 'not_started' : 'completed'
    setStageStatus(s => ({ ...s, [stageId]: newStatus }))
    updateUserProgress(user.user_id, stageId, newStatus).catch(() => {})
  }

  const totalStages = selected?.stages.length || 1
  const completedCount = selected?.stages.filter(s => stageStatus[s.id] === 'completed').length || 0
  const progressPct = Math.round((completedCount / totalStages) * 100)

  return (
    <div>
      <h2><Map size={22} style={{ verticalAlign: 'text-bottom', marginRight: 6 }} />Career Roadmap</h2>

      {!selected && (
        <div className="feature-grid" style={{ marginTop: 8 }}>
          {roadmaps.map(r => (
            <div key={r.role_name} className="card card-hover" style={{ cursor: 'pointer' }} onClick={() => openRoadmap(r)}>
              <h4>{r.role_name}</h4>
              <p style={{ color: 'var(--color-muted)', fontSize: 13 }}>{r.description}</p>
              <p style={{ fontSize: 12, color: 'var(--color-muted)' }}>{r.stages.length} stages</p>
            </div>
          ))}
        </div>
      )}

      {selected && (
        <div>
          <button className="btn-ghost" style={{ marginBottom: 16 }} onClick={() => setSelected(null)}>← Back</button>
          <h3>{selected.role_name.toUpperCase()}</h3>
          <div className="progress-bar-track" style={{ marginBottom: 8 }}>
            <div className="progress-bar-fill" style={{ width: `${progressPct}%` }} />
          </div>
          <p>Progress: {progressPct}% ({completedCount} of {totalStages} stages)</p>
          {!isAuthenticated && (
            <p style={{ fontSize: 13, color: 'var(--color-muted)' }}>Log in to save your progress across visits.</p>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 12 }}>
            {selected.stages.map(stage => {
              const done = stageStatus[stage.id] === 'completed'
              return (
                <div key={stage.id} className="card" style={{ borderColor: done ? '#bbf7d0' : undefined }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div onClick={() => setActiveStage(activeStage === stage.id ? null : stage.id)}
                      style={{ cursor: 'pointer', flex: 1, display: 'flex', alignItems: 'center', gap: 8 }}>
                      {done && <CheckCircle2 size={18} color="#16a34a" />}
                      <b>{stage.title}</b>
                    </div>
                    <input type="checkbox" checked={done} onChange={() => toggleComplete(stage.id)} />
                  </div>

                  {activeStage === stage.id && (
                    <div style={{ marginTop: 10 }}>
                      <p><b>Topics:</b> {stage.topics.join(', ')}</p>
                      <p><b>Skills:</b> {stage.skills.map(s => <span key={s} className="skill-badge">{s}</span>)}</p>
                      {stage.suggested_project && <p><b>Suggested Project:</b> {stage.suggested_project}</p>}
                      {stage.estimated_hours && <p><b>Estimated Time:</b> ~{stage.estimated_hours} hours</p>}
                      {stage.prerequisites.length > 0 && <p><b>Prerequisites:</b> {stage.prerequisites.join(', ')}</p>}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
