"""
Skill Demand Analysis
----------------------
All percentages here are CALCULATED from the jobs currently in the database
-- nothing is hard-coded. Swap in a bigger dataset and the numbers update
automatically.
"""
from collections import Counter
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.models import Job, JobSkill, Skill


def get_skill_demand(db: Session, role: Optional[str] = None,
                      location: Optional[str] = None,
                      experience: Optional[str] = None):
    query = db.query(Job)
    if role:
        query = query.filter(Job.job_title.ilike(f"%{role}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if experience:
        query = query.filter(Job.experience.ilike(f"%{experience}%"))

    jobs = query.all()
    total_jobs = len(jobs) or 1  # avoid divide-by-zero

    counter = Counter()
    for job in jobs:
        for js in job.job_skills:
            counter[js.skill.name] += 1

    results = [
        {"skill": skill, "count": count, "percentage": round(count / total_jobs * 100, 1)}
        for skill, count in counter.most_common()
    ]
    return results, total_jobs


def compare_roles(db: Session, roles: List[str]):
    """Return {role: [{skill, percentage}, ...]} for each requested role."""
    comparison = {}
    for role in roles:
        demand, _ = get_skill_demand(db, role=role)
        comparison[role] = demand
    return comparison


def get_skill_combinations(db: Session, top_n: int = 15):
    """Find which skill pairs most frequently co-occur within the same job."""
    from itertools import combinations
    pair_counter = Counter()

    jobs = db.query(Job).all()
    for job in jobs:
        skill_names = sorted({js.skill.name for js in job.job_skills})
        for pair in combinations(skill_names, 2):
            pair_counter[pair] += 1

    total = len(jobs) or 1
    top_pairs = [
        {"skills": list(pair), "count": count, "percentage": round(count / total * 100, 1)}
        for pair, count in pair_counter.most_common(top_n)
    ]
    return top_pairs
