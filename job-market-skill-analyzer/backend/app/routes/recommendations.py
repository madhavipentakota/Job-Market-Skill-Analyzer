from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.services.roadmap.recommendation import recommend_next_skills

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.get("/recommendations")
def recommendations(
    target_role: str,
    current_skills: Optional[str] = Query(None, description="Comma-separated skill names"),
    db: Session = Depends(get_db),
):
    skills_list = [s.strip() for s in current_skills.split(",")] if current_skills else []
    return recommend_next_skills(db, target_role, skills_list)
