import { useEffect, useState } from 'react'
import { LineChart as LineChartIcon, CheckCircle2, Circle, Clock } from 'lucide-react'
import { getUserProgress } from '../services/api.js'
import { useAuth } from '../context/AuthContext.jsx'

const ACTIVE_ROADMAP_KEY = 'jmsa_active_roadmap'

export default function MyProgress() {
  const [progress, setProgress] = useState(null)
  const [loading, setLoading] = useState(true)
  const { user, isAuthenticated } = useAuth()
  const activeRoadmap = localStorage.getItem(ACTIVE_ROADMAP_KEY)

  useEffect(() => {
    if (!isAuthenticated) { setLoading(false); return }
    // Scope to the roadmap the user last opened, so the denominator is that
    // roadmap's real stage count (this is what fixes the "100% after one
    // checkbox" bug — the old version had no fixed roadmap to measure against).
    getUserProgress(user.user_id, activeRoadmap || undefined)
      .then(setProgress)
      .finally(() => setLoading(false))
  }, [isAuthenticated])

  if (!isAuthenticated) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: 48 }}>
        <h3>Log in to see your progress</h3>
        <p style={{ color: 'var(--color-muted)' }}>Your roadmap progress is saved to your account.</p>
      </div>
    )
  }

  if (loading) return <p>Loading progress...</p>
  if (!progress || progress.total_stages === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: 48 }}>
        <h3>No progress yet</h3>
        <p style={{ color: 'var(--color-muted)' }}>
          Visit <b>Career Roadmap</b>, pick a path, and start checking off stages.
        </p>
      </div>
    )
  }

  return (
    <div>
      <h2><LineChartIcon size={22} style={{ verticalAlign: 'text-bottom', marginRight: 6 }} />My Progress</h2>
      <div className="card">
        <h3>Overall Progress: {progress.overall_progress_percentage}%</h3>
        <div className="progress-bar-track">
          <div className="progress-bar-fill" style={{ width: `${progress.overall_progress_percentage}%` }} />
        </div>
        <p style={{ color: 'var(--color-muted)', fontSize: 13, marginTop: 6 }}>
          {progress.completed_stages} of {progress.total_stages} stages completed
          {progress.role ? ` — ${progress.role}` : ''}
        </p>
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <h4>Stage Status</h4>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {progress.stages.map(s => (
            <div key={s.stage_id} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '6px 0', borderBottom: '1px solid var(--color-border)' }}>
              <StatusIcon status={s.status} />
              <span style={{ flex: 1 }}>{s.title}</span>
              <span style={{ fontSize: 12, color: 'var(--color-muted)', textTransform: 'capitalize' }}>{s.status.replace('_', ' ')}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function StatusIcon({ status }) {
  if (status === 'completed') return <CheckCircle2 size={18} color="#16a34a" />
  if (status === 'in_progress') return <Clock size={18} color="#f59e0b" />
  return <Circle size={18} color="#cbd5e1" />
}
