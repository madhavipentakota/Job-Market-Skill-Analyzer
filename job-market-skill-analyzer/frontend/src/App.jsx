import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext.jsx'
import Navbar from './components/Navbar.jsx'
import Home from './pages/Home.jsx'
import Dashboard from './pages/Dashboard.jsx'
import JobExplorer from './pages/JobExplorer.jsx'
import SkillDemand from './pages/SkillDemand.jsx'
import CompareRoles from './pages/CompareRoles.jsx'
import SkillCombinations from './pages/SkillCombinations.jsx'
import SkillGap from './pages/SkillGap.jsx'
import CareerRoadmap from './pages/CareerRoadmap.jsx'
import MyProgress from './pages/MyProgress.jsx'

export default function App() {
  return (
    <AuthProvider>
      <div className="app-shell">
        <Navbar />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/explorer" element={<JobExplorer />} />
            <Route path="/skill-demand" element={<SkillDemand />} />
            <Route path="/compare-roles" element={<CompareRoles />} />
            <Route path="/skill-combinations" element={<SkillCombinations />} />
            <Route path="/skill-gap" element={<SkillGap />} />
            <Route path="/roadmap" element={<CareerRoadmap />} />
            <Route path="/progress" element={<MyProgress />} />
          </Routes>
        </div>
      </div>
    </AuthProvider>
  )
}
