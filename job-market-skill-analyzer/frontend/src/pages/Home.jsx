import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  BarChart3, Brain, Target, Map, ArrowRight, Database,
  Sparkles, ListChecks, TrendingUp, GitCompare,
} from 'lucide-react'
import { getJobs, getSkills, getRoles, getLocations } from '../services/api.js'
import { useAuth } from '../context/AuthContext.jsx'
import AuthModal from '../components/AuthModal.jsx'

const PIPELINE = [
  { icon: Database, label: 'Job Data' },
  { icon: Brain, label: 'NLP Skill Extraction' },
  { icon: TrendingUp, label: 'Skill Demand Analysis' },
  { icon: Target, label: 'Skill Gap Analysis' },
  { icon: Map, label: 'Personalized Roadmap' },
]

const FEATURES = [
  { icon: BarChart3, color: '#4f46e5', title: 'Job Market Explorer', desc: 'Filter real postings by role, location, experience and skill, and see exactly what each job asks for.' },
  { icon: TrendingUp, color: '#f59e0b', title: 'Skill Demand Analytics', desc: 'See what percentage of postings require each skill — calculated live from the dataset, never hard-coded.' },
  { icon: GitCompare, color: '#0ea5e9', title: 'Compare Job Roles', desc: 'Put two roles side by side — e.g. Data Analyst vs Data Scientist — and see where their skill demands diverge.' },
  { icon: Target, color: '#dc2626', title: 'Skill Gap Analyzer', desc: 'Enter what you already know and instantly see what a target role still requires from you.' },
  { icon: Map, color: '#16a34a', title: 'Personalized Roadmap', desc: 'A stage-by-stage learning path that skips what you already know and prioritizes what the market wants.' },
  { icon: ListChecks, color: '#7c3aed', title: 'Progress Tracking', desc: 'Check off roadmap stages as you complete them and watch your readiness score climb.' },
]

export default function Home() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const [stats, setStats] = useState({ jobs: 0, skills: 0, roles: 0, locations: 0 })
  const [authMode, setAuthMode] = useState(null)

  useEffect(() => {
    Promise.all([getJobs(), getSkills(), getRoles(), getLocations()])
      .then(([jobs, skills, roles, locations]) => {
        setStats({ jobs: jobs.length, skills: skills.length, roles: roles.length, locations: locations.length })
      })
      .catch(() => {})
  }, [])

  const goOrSignup = (path) => {
    if (isAuthenticated) navigate(path)
    else setAuthMode('signup')
  }

  return (
    <div>
      {/* ---------- Hero ---------- */}
      <section className="hero">
        <div>
          <span className="hero-badge"><Sparkles size={14} /> Data Science + NLP powered</span>
          <h1>Understand what companies <span>actually</span> want.</h1>
          <p className="lead">
            Analyze real job postings, extract the skills companies are hiring for with NLP,
            compare them against your own skills, and follow a personalized roadmap to close the gap.
          </p>
          <div className="hero-ctas">
            <button className="btn" onClick={() => navigate('/explorer')}>
              Explore Job Market <ArrowRight size={16} />
            </button>
            <button className="btn-outline" onClick={() => goOrSignup('/skill-gap')}>Analyze My Skills</button>
            <button className="btn-outline" onClick={() => goOrSignup('/roadmap')}>Build My Roadmap</button>
          </div>
        </div>

        {/* CSS-illustrated visual (no external image hosting required) */}
        <div className="hero-visual">
          <div className="glass-card" style={{ top: '10%', left: '8%' }}>
            <TrendingUp size={16} style={{ color: '#4f46e5', marginBottom: 4 }} /><br />
            Python — 84% demand
          </div>
          <div className="glass-card" style={{ top: '42%', right: '6%' }}>
            <Target size={16} style={{ color: '#dc2626', marginBottom: 4 }} /><br />
            Skill Readiness: 62%
          </div>
          <div className="glass-card" style={{ bottom: '10%', left: '14%' }}>
            <Map size={16} style={{ color: '#16a34a', marginBottom: 4 }} /><br />
            Stage 4 of 11 complete
          </div>
        </div>
      </section>

      {/* ---------- Stats ---------- */}
      <div className="card stats-strip">
        <StatBox num={stats.jobs} label="Jobs Analyzed" />
        <StatBox num={stats.skills} label="Skills Identified" />
        <StatBox num={stats.roles} label="Job Roles" />
        <StatBox num={stats.locations} label="Locations" />
      </div>
      <p style={{ textAlign: 'center', color: 'var(--color-muted)', fontSize: 13, marginTop: -24 }}>
        Built on a sample dataset for demonstration.<span className="demo-tag">DEMO DATA</span>
        &nbsp;Swap in a larger CSV to scale up.
      </p>

      {/* ---------- Pipeline ---------- */}
      <div className="section-title" style={{ marginTop: 56 }}>
        <h2>How It Works</h2>
        <p>One continuous pipeline from raw job postings to a plan you can actually follow.</p>
      </div>
      <div className="pipeline">
        {PIPELINE.map((step, i) => (
          <div key={step.label} style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div className="pipeline-step">
              <div className="icon-wrap"><step.icon size={20} /></div>
              {step.label}
            </div>
            {i < PIPELINE.length - 1 && <ArrowRight className="pipeline-arrow" size={20} />}
          </div>
        ))}
      </div>

      {/* ---------- Features ---------- */}
      <div className="section-title" style={{ marginTop: 56 }}>
        <h2>Everything you need, end to end</h2>
        <p>From exploring the raw market to tracking your own learning progress.</p>
      </div>
      <div className="feature-grid">
        {FEATURES.map(f => (
          <div key={f.title} className="card card-hover feature-card">
            <div className="icon-wrap" style={{ background: `${f.color}1a`, color: f.color }}>
              <f.icon size={22} />
            </div>
            <h4>{f.title}</h4>
            <p>{f.desc}</p>
          </div>
        ))}
      </div>

      {/* ---------- CTA ---------- */}
      <div className="cta-band">
        <h2>Ready to see your own skill gap?</h2>
        <p>Create a free account to save your skills and track roadmap progress over time.</p>
        <button className="btn" onClick={() => goOrSignup('/skill-gap')}>
          {isAuthenticated ? 'Analyze My Skills' : 'Sign Up Free'} <ArrowRight size={16} />
        </button>
      </div>

      {authMode && <AuthModal mode={authMode} onClose={() => setAuthMode(null)} />}
    </div>
  )
}

function StatBox({ num, label }) {
  return (
    <div className="stat-box">
      <div className="num">{num}</div>
      <div className="label">{label}</div>
    </div>
  )
}
