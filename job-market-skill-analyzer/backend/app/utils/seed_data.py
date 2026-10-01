"""
One-time (idempotent-ish) seed script.

Loads data/jobs.csv, runs NLP skill extraction on each job description,
populates jobs/skills/job_skills, and loads the predefined roadmap
templates into career_roadmaps/roadmap_stages.

Run:
    cd backend
    python -m app.utils.seed_data
"""
import json
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.db import Base, engine, SessionLocal
from app.models.models import Job, Skill, JobSkill, CareerRoadmap, RoadmapStage
from app.services.nlp.skill_extractor import extract_skills, SKILL_DICTIONARY
from app.services.roadmap.roadmap_data import ALL_ROADMAPS

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "jobs.csv")


def seed_skills(db):
    existing = {s.name for s in db.query(Skill).all()}
    for name in SKILL_DICTIONARY:
        if name not in existing:
            db.add(Skill(name=name))
    db.commit()


def seed_jobs(db):
    if db.query(Job).count() > 0:
        print("Jobs already seeded, skipping.")
        return

    df = pd.read_csv(CSV_PATH)
    skill_lookup = {s.name: s for s in db.query(Skill).all()}

    for _, row in df.iterrows():
        job = Job(
            job_title=row["job_title"],
            company=row.get("company"),
            location=row.get("location"),
            experience=row.get("experience"),
            salary=str(row.get("salary")) if not pd.isna(row.get("salary")) else None,
            job_description=row.get("job_description"),
            is_demo_data=1,
        )
        db.add(job)
        db.flush()  # get job.id

        detected = extract_skills(str(row.get("job_description", "")))
        for skill_name in detected:
            skill = skill_lookup.get(skill_name)
            if not skill:
                skill = Skill(name=skill_name)
                db.add(skill)
                db.flush()
                skill_lookup[skill_name] = skill
            db.add(JobSkill(job_id=job.id, skill_id=skill.id))

    db.commit()
    print(f"Seeded {len(df)} jobs.")


def seed_roadmaps(db):
    if db.query(CareerRoadmap).count() > 0:
        print("Roadmaps already seeded, skipping.")
        return

    for roadmap_def in ALL_ROADMAPS:
        roadmap = CareerRoadmap(
            role_name=roadmap_def["role_name"],
            description=roadmap_def["description"],
        )
        db.add(roadmap)
        db.flush()

        for i, stage_def in enumerate(roadmap_def["stages"], start=1):
            db.add(RoadmapStage(
                roadmap_id=roadmap.id,
                stage_order=i,
                title=stage_def["title"],
                topics=json.dumps(stage_def["topics"]),
                skills=json.dumps(stage_def["skills"]),
                suggested_project=stage_def.get("suggested_project"),
                estimated_hours=stage_def.get("estimated_hours"),
                prerequisites=json.dumps(stage_def.get("prerequisites", [])),
            ))
    db.commit()
    print(f"Seeded {len(ALL_ROADMAPS)} roadmaps.")


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_skills(db)
        seed_jobs(db)
        seed_roadmaps(db)
        print("Seeding complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
