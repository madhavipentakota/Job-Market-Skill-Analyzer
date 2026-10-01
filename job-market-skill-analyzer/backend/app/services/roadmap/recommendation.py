"""
Recommendation Engine
-----------------------
Combines:
  1. Skill-gap output (missing skills for the target role)
  2. Job-market demand (percentage of postings requiring each skill)
  3. Roadmap prerequisite structure (a skill isn't recommended before its
     prerequisite stage's skills are already covered)

...to produce a prioritized "what to learn next" list.
"""
from typing import List
from sqlalchemy.orm import Session
from app.services.analytics.skill_gap import analyze_skill_gap
from app.models.models import CareerRoadmap


def recommend_next_skills(db: Session, target_role: str, current_skills: List[str], top_n: int = 5):
    gap = analyze_skill_gap(db, target_role, current_skills)
    missing_ranked = gap["high_priority"] + [
        s for s in gap["missing"] if s not in gap["high_priority"]
    ]

    roadmap = db.query(CareerRoadmap).filter(
        CareerRoadmap.role_name.ilike(f"%{target_role}%")
    ).first()

    if roadmap:
        # Reorder missing skills to match the order they first appear in the
        # roadmap's stages, so prerequisites naturally come first.
        stage_skill_order = []
        for stage in roadmap.stages:
            import json
            for s in json.loads(stage.skills):
                if s not in stage_skill_order:
                    stage_skill_order.append(s)

        def sort_key(skill):
            return stage_skill_order.index(skill) if skill in stage_skill_order else len(stage_skill_order)

        missing_ranked = sorted(set(missing_ranked), key=sort_key)

    recommended = missing_ranked[:top_n]

    already_count = len(gap["already_have"])
    message = (
        f"You already have {already_count} skill(s) relevant to {target_role}. "
        f"Based on job-market demand and the {target_role} roadmap, your next "
        f"recommended skills are: {', '.join(recommended) if recommended else 'none — you are well covered!'}"
    )

    return {
        "target_role": target_role,
        "current_skills": current_skills,
        "recommended_skills": recommended,
        "message": message,
    }
