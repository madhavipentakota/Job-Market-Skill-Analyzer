"""
Skill Gap Analysis
-------------------
Compares a student's current skills against the skills required for a
target role (derived from real job postings in the DB) and buckets each
required skill into: already_have / missing / partially_covered.

"Readiness %" = (skills the student already has) / (skills required for
the role) -- expressed as coverage of THIS dataset's requirements only.
It is explicitly not framed as an employability guarantee.
"""
from typing import List
from sqlalchemy.orm import Session
from app.services.analytics.skill_demand import get_skill_demand
from app.services.nlp.skill_extractor import normalize_skill_name

# A skill counted as "required" if it appears in at least this % of jobs
# for the target role. Below that, it's "partially covered" territory
# (nice-to-have rather than core requirement).
CORE_SKILL_THRESHOLD = 30.0
HIGH_PRIORITY_THRESHOLD = 60.0


def analyze_skill_gap(db: Session, target_role: str, current_skills: List[str]):
    demand, _ = get_skill_demand(db, role=target_role)

    normalized_current = {normalize_skill_name(s) for s in current_skills}

    already_have, missing, partially_covered, high_priority = [], [], [], []

    for item in demand:
        skill = item["skill"]
        pct = item["percentage"]
        if skill in normalized_current:
            already_have.append(skill)
            continue
        if pct >= CORE_SKILL_THRESHOLD:
            missing.append(skill)
            if pct >= HIGH_PRIORITY_THRESHOLD:
                high_priority.append(skill)
        else:
            partially_covered.append(skill)

    required_core_count = len(already_have) + len(missing)
    readiness = round((len(already_have) / required_core_count) * 100, 1) if required_core_count else 0.0

    return {
        "target_role": target_role,
        "already_have": already_have,
        "missing": missing,
        "partially_covered": partially_covered,
        "high_priority": high_priority,
        "readiness_percentage": readiness,
    }
