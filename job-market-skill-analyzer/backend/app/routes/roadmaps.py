import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.models import CareerRoadmap
from app.schemas.schemas import RoadmapOut

router = APIRouter(prefix="/api", tags=["roadmaps"])


@router.get("/roadmaps", response_model=List[RoadmapOut])
def list_roadmaps(db: Session = Depends(get_db)):
    roadmaps = db.query(CareerRoadmap).all()
    return [_to_roadmap_out(r) for r in roadmaps]


@router.get("/roadmaps/{role}", response_model=RoadmapOut)
def get_roadmap(role: str, db: Session = Depends(get_db)):
    roadmap = db.query(CareerRoadmap).filter(CareerRoadmap.role_name.ilike(f"%{role}%")).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return _to_roadmap_out(roadmap)


def _to_roadmap_out(r: CareerRoadmap) -> dict:
    return {
        "role_name": r.role_name,
        "description": r.description,
        "stages": [
            {
                "id": s.id,
                "stage_order": s.stage_order,
                "title": s.title,
                "topics": json.loads(s.topics or "[]"),
                "skills": json.loads(s.skills or "[]"),
                "suggested_project": s.suggested_project,
                "estimated_hours": s.estimated_hours,
                "prerequisites": json.loads(s.prerequisites or "[]"),
            }
            for s in r.stages
        ],
    }
