from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.db import get_db
from app.models.models import Skill
from app.services.analytics.skill_demand import get_skill_demand, compare_roles, get_skill_combinations
from app.schemas.schemas import RoleCompareRequest

router = APIRouter(prefix="/api", tags=["skills"])


@router.get("/skills")
def list_skills(db: Session = Depends(get_db)):
    return [s.name for s in db.query(Skill).all()]


@router.get("/skills/demand")
def skill_demand(
    role: Optional[str] = None,
    location: Optional[str] = None,
    experience: Optional[str] = None,
    db: Session = Depends(get_db),
):
    results, total_jobs = get_skill_demand(db, role=role, location=location, experience=experience)
    return {"total_jobs_considered": total_jobs, "skills": results}


@router.get("/skills/combinations")
def skill_combinations(top_n: int = 15, db: Session = Depends(get_db)):
    return {"pairs": get_skill_combinations(db, top_n=top_n)}


@router.post("/roles/compare")
def role_compare(payload: RoleCompareRequest, db: Session = Depends(get_db)):
    return compare_roles(db, roles=payload.roles)
