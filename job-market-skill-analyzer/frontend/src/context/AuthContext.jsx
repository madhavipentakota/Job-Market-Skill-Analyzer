import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const stored = localStorage.getItem('jmsa_user')
    if (stored) {
      try { setUser(JSON.parse(stored)) } catch { /* ignore corrupt data */ }
    }
  }, [])

  const login = (userData) => {
    setUser(userData)
    localStorage.setItem('jmsa_user', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('jmsa_user')
    localStorage.removeItem('jmsa_active_roadmap')
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
