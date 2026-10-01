"""
Job Market Skill Analyzer -- FastAPI entrypoint.

Run locally:
    uvicorn app.main:app --reload --port 8000

Docs available at:
    http://localhost:8000/docs
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.database.db import Base, engine
from app.routes import jobs, skills, skill_gap, roadmaps, user, recommendations, auth

load_dotenv()

# Create tables on startup if they don't exist yet (SQLite-friendly).
# For production Postgres, prefer Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Market Skill Analyzer API",
    description="Analyzes job-market data, extracts in-demand skills, "
                 "finds skill gaps, and builds personalized learning roadmaps.",
    version="1.0.0",
)

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(skills.router)
app.include_router(skill_gap.router)
app.include_router(roadmaps.router)
app.include_router(user.router)
app.include_router(recommendations.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Job Market Skill Analyzer API is running. See /docs for API documentation."}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
