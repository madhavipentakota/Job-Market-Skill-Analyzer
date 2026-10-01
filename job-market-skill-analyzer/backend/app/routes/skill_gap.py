from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import SkillGapRequest, SkillGapResponse
from app.services.analytics.skill_gap import analyze_skill_gap

router = APIRouter(prefix="/api", tags=["skill-gap"])


@router.post("/skill-gap", response_model=SkillGapResponse)
def skill_gap(payload: SkillGapRequest, db: Session = Depends(get_db)):
    return analyze_skill_gap(db, payload.target_role, payload.current_skills)
