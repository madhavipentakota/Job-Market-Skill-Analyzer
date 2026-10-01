from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database.db import get_db
from app.models.models import Job
from app.schemas.schemas import JobOut

router = APIRouter(prefix="/api", tags=["jobs"])


@router.get("/jobs", response_model=List[JobOut])
def list_jobs(
    role: Optional[str] = None,
    location: Optional[str] = None,
    experience: Optional[str] = None,
    skill: Optional[str] = None,
    company: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Job)
    if role:
        query = query.filter(Job.job_title.ilike(f"%{role}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if experience:
        query = query.filter(Job.experience.ilike(f"%{experience}%"))
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if search:
        query = query.filter(Job.job_title.ilike(f"%{search}%"))

    jobs = query.all()
    if skill:
        jobs = [j for j in jobs if any(js.skill.name.lower() == skill.lower() for js in j.job_skills)]

    return [_to_job_out(j) for j in jobs]


@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return _to_job_out(job)


@router.get("/roles")
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Job.job_title).distinct().all()
    return sorted({r[0] for r in roles})


@router.get("/locations")
def list_locations(db: Session = Depends(get_db)):
    locations = db.query(Job.location).distinct().all()
    return sorted({l[0] for l in locations if l[0]})


def _to_job_out(job: Job) -> dict:
    return {
        "id": job.id,
        "job_title": job.job_title,
        "company": job.company,
        "location": job.location,
        "experience": job.experience,
        "salary": job.salary,
        "skills": [js.skill.name for js in job.job_skills],
        "is_demo_data": bool(job.is_demo_data),
    }
