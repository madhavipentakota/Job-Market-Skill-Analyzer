"""
Pydantic schemas used for request/response validation.
Keep these in sync with app/models/models.py
"""
from pydantic import BaseModel
from typing import List, Optional


class JobOut(BaseModel):
    id: int
    job_title: str
    company: Optional[str]
    location: Optional[str]
    experience: Optional[str]
    salary: Optional[str]
    skills: List[str] = []
    is_demo_data: bool = True

    class Config:
        from_attributes = True


class SkillDemandItem(BaseModel):
    skill: str
    count: int
    percentage: float


class RoleCompareRequest(BaseModel):
    roles: List[str]
    skills: Optional[List[str]] = None  # optional: restrict comparison to these skills


class SkillGapRequest(BaseModel):
    target_role: str
    current_skills: List[str]


class SkillGapResponse(BaseModel):
    target_role: str
    already_have: List[str]
    missing: List[str]
    partially_covered: List[str]
    high_priority: List[str]
    readiness_percentage: float


class RoadmapStageOut(BaseModel):
    id: int
    stage_order: int
    title: str
    topics: List[str]
    skills: List[str]
    suggested_project: Optional[str]
    estimated_hours: Optional[int]
    prerequisites: List[str] = []

    class Config:
        from_attributes = True


class RoadmapOut(BaseModel):
    role_name: str
    description: Optional[str]
    stages: List[RoadmapStageOut]

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    user_id: int
    email: str
    full_name: Optional[str] = None
    target_role: Optional[str] = None


class UserSkillsIn(BaseModel):
    user_id: int
    skills: List[str]


class UserProgressIn(BaseModel):
    user_id: int
    stage_id: int
    status: str  # not_started | in_progress | completed


class RecommendationResponse(BaseModel):
    target_role: str
    current_skills: List[str]
    recommended_skills: List[str]
    message: str
