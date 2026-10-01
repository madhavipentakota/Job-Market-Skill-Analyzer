import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({ baseURL: API_BASE_URL, timeout: 10000 })

// Auth
export const registerUser = (email, password, full_name) =>
  api.post('/auth/register', { email, password, full_name }).then(r => r.data)
export const loginUser = (email, password) =>
  api.post('/auth/login', { email, password }).then(r => r.data)

// Jobs
export const getJobs = (params) => api.get('/jobs', { params }).then(r => r.data)
export const getJob = (id) => api.get(`/jobs/${id}`).then(r => r.data)
export const getRoles = () => api.get('/roles').then(r => r.data)
export const getLocations = () => api.get('/locations').then(r => r.data)

// Skills
export const getSkills = () => api.get('/skills').then(r => r.data)
export const getSkillDemand = (params) => api.get('/skills/demand', { params }).then(r => r.data)
export const getSkillCombinations = (top_n = 15) =>
  api.get('/skills/combinations', { params: { top_n } }).then(r => r.data)
export const compareRoles = (roles) => api.post('/roles/compare', { roles }).then(r => r.data)

// Skill gap
export const analyzeSkillGap = (target_role, current_skills) =>
  api.post('/skill-gap', { target_role, current_skills }).then(r => r.data)

// Roadmaps
export const getRoadmaps = () => api.get('/roadmaps').then(r => r.data)
export const getRoadmap = (role) => api.get(`/roadmaps/${role}`).then(r => r.data)

// User / progress
export const saveUserSkills = (user_id, skills) =>
  api.post('/user/skills', { user_id, skills }).then(r => r.data)
export const getUserProgress = (user_id, role) =>
  api.get('/user/progress', { params: { user_id, role } }).then(r => r.data)
export const updateUserProgress = (user_id, stage_id, status) =>
  api.post('/user/progress', { user_id, stage_id, status }).then(r => r.data)

// Recommendations
export const getRecommendations = (target_role, current_skills = []) =>
  api.get('/recommendations', {
    params: { target_role, current_skills: current_skills.join(',') },
  }).then(r => r.data)

export default api
