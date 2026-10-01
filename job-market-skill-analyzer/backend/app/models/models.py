"""
SQLAlchemy ORM models.

Tables:
- User            : registered users (optional auth)
- Job             : job postings (from CSV / dataset)
- Skill           : master skill dictionary
- JobSkill        : many-to-many link between Job and Skill (extracted per job)
- CareerRoadmap   : roadmap definitions (e.g. "Data Science")
- RoadmapStage     : ordered stages within a roadmap
- UserSkill       : skills a user says they already have
- UserProgress    : per-user, per-stage completion status
"""
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, DateTime, Text, Table
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    target_role = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True, nullable=False)
    company = Column(String, index=True)
    location = Column(String, index=True)
    experience = Column(String)          # e.g. "0-2 years"
    salary = Column(String, nullable=True)  # kept as string/range; parsed for charts
    job_description = Column(Text)
    is_demo_data = Column(Integer, default=1)  # 1 = sample/demo dataset

    job_skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # normalized name
    category = Column(String, nullable=True)  # e.g. "Programming", "ML", "Tool"

    job_skills = relationship("JobSkill", back_populates="skill")
    user_skills = relationship("UserSkill", back_populates="skill")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    job = relationship("Job", back_populates="job_skills")
    skill = relationship("Skill", back_populates="job_skills")


class CareerRoadmap(Base):
    __tablename__ = "career_roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True, nullable=False)  # e.g. "Data Science"
    description = Column(Text, nullable=True)

    stages = relationship("RoadmapStage", back_populates="roadmap",
                           order_by="RoadmapStage.stage_order",
                           cascade="all, delete-orphan")


class RoadmapStage(Base):
    __tablename__ = "roadmap_stages"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("career_roadmaps.id"), nullable=False)
    stage_order = Column(Integer, nullable=False)
    title = Column(String, nullable=False)         # "Stage 1: Python Fundamentals"
    topics = Column(Text)                            # JSON-encoded list of topics
    skills = Column(Text)                             # JSON-encoded list of skill names
    suggested_project = Column(String, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    prerequisites = Column(Text, nullable=True)       # JSON-encoded list of prior stage titles

    roadmap = relationship("CareerRoadmap", back_populates="stages")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stage_id = Column(Integer, ForeignKey("roadmap_stages.id"), nullable=False)
    status = Column(String, default="not_started")  # not_started | in_progress | completed
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="progress")
    stage = relationship("RoadmapStage")
