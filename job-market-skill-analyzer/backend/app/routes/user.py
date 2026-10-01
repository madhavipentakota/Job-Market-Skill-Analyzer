from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database.db import get_db
from app.models.models import UserSkill, UserProgress, Skill, CareerRoadmap, RoadmapStage
from app.schemas.schemas import UserSkillsIn, UserProgressIn
from app.services.nlp.skill_extractor import normalize_skill_name

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/skills")
def set_user_skills(payload: UserSkillsIn, db: Session = Depends(get_db)):
    db.query(UserSkill).filter(UserSkill.user_id == payload.user_id).delete()
    for raw in payload.skills:
        name = normalize_skill_name(raw)
        skill = db.query(Skill).filter(Skill.name == name).first()
        if not skill:
            skill = Skill(name=name)
            db.add(skill)
            db.flush()
        db.add(UserSkill(user_id=payload.user_id, skill_id=skill.id))
    db.commit()
    return {"status": "ok", "skills_saved": len(payload.skills)}


@router.get("/progress")
def get_progress(user_id: int, role: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Progress is always calculated against the TOTAL number of stages in a
    roadmap, not just the stages the user has touched -- that mismatch was
    the bug that made checking a single box show 100%.

    If `role` is given, scope to that one roadmap. If omitted, aggregate
    across every roadmap the user has any progress in.
    """
    if role:
        roadmap = db.query(CareerRoadmap).filter(CareerRoadmap.role_name.ilike(f"%{role}%")).first()
        if not roadmap:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        roadmaps = [roadmap]
    else:
        touched_roadmap_ids = (
            db.query(RoadmapStage.roadmap_id)
            .join(UserProgress, UserProgress.stage_id == RoadmapStage.id)
            .filter(UserProgress.user_id == user_id)
            .distinct()
            .all()
        )
        ids = [r[0] for r in touched_roadmap_ids]
        roadmaps = db.query(CareerRoadmap).filter(CareerRoadmap.id.in_(ids)).all() if ids else []

    progress_rows = {
        p.stage_id: p.status
        for p in db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    }

    all_stages = []
    for rm in roadmaps:
        for stage in rm.stages:
            all_stages.append({
                "stage_id": stage.id,
                "roadmap": rm.role_name,
                "title": stage.title,
                "status": progress_rows.get(stage.id, "not_started"),
            })

    total = len(all_stages) or 1
    completed = sum(1 for s in all_stages if s["status"] == "completed")

    return {
        "user_id": user_id,
        "role": role,
        "overall_progress_percentage": round(completed / total * 100, 1) if all_stages else 0.0,
        "total_stages": len(all_stages),
        "completed_stages": completed,
        "stages": all_stages,
    }


@router.post("/progress")
def update_progress(payload: UserProgressIn, db: Session = Depends(get_db)):
    row = db.query(UserProgress).filter(
        UserProgress.user_id == payload.user_id,
        UserProgress.stage_id == payload.stage_id,
    ).first()
    if row:
        row.status = payload.status
    else:
        row = UserProgress(user_id=payload.user_id, stage_id=payload.stage_id, status=payload.status)
        db.add(row)
    db.commit()
    return {"status": "ok"}
