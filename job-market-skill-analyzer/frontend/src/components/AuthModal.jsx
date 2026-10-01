import { useState } from 'react'
import { X, Mail, Lock, User, Loader2 } from 'lucide-react'
import { loginUser, registerUser } from '../services/api.js'
import { useAuth } from '../context/AuthContext.jsx'

export default function AuthModal({ mode: initialMode, onClose }) {
  const [mode, setMode] = useState(initialMode) // 'login' | 'signup'
  const [form, setForm] = useState({ full_name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()

  const update = (field) => (e) => setForm(f => ({ ...f, [field]: e.target.value }))

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = mode === 'signup'
        ? await registerUser(form.email, form.password, form.full_name)
        : await loginUser(form.email, form.password)
      login(data)
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-panel" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} aria-label="Close"><X size={20} /></button>

        <div className="modal-tabs">
          <button className={mode === 'login' ? 'active' : ''} onClick={() => setMode('login')}>Log In</button>
          <button className={mode === 'signup' ? 'active' : ''} onClick={() => setMode('signup')}>Sign Up</button>
        </div>

        <h2 style={{ marginTop: 4 }}>{mode === 'login' ? 'Welcome back' : 'Create your account'}</h2>
        <p style={{ color: 'var(--color-muted)', marginTop: -8, marginBottom: 20 }}>
          {mode === 'login' ? 'Log in to track your roadmap progress.' : 'Sign up to save your skills and track progress.'}
        </p>

        <form onSubmit={submit} className="auth-form">
          {mode === 'signup' && (
            <div className="field">
              <User size={18} className="field-icon" />
              <input required placeholder=" " value={form.full_name} onChange={update('full_name')} />
              <label>Full name</label>
            </div>
          )}
          <div className="field">
            <Mail size={18} className="field-icon" />
            <input required type="email" placeholder=" " value={form.email} onChange={update('email')} />
            <label>Email</label>
          </div>
          <div className="field">
            <Lock size={18} className="field-icon" />
            <input required type="password" minLength={4} placeholder=" " value={form.password} onChange={update('password')} />
            <label>Password</label>
          </div>

          {error && <div className="form-error">{error}</div>}

          <button className="btn btn-block" type="submit" disabled={loading}>
            {loading ? <Loader2 size={18} className="spin" /> : (mode === 'login' ? 'Log In' : 'Create Account')}
          </button>
        </form>

        <p style={{ fontSize: 13, color: 'var(--color-muted)', textAlign: 'center', marginTop: 16 }}>
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <a href="#" onClick={(e) => { e.preventDefault(); setMode(mode === 'login' ? 'signup' : 'login') }}>
            {mode === 'login' ? 'Sign up' : 'Log in'}
          </a>
        </p>
      </div>
    </div>
  )
}
