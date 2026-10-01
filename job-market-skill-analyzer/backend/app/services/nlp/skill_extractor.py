"""
NLP Skill Extraction
---------------------
Given a job_description string, detect which known skills are mentioned.

Approach (kept intentionally simple + explainable for a viva):
1. Lowercase + clean the text.
2. Build a normalization map so aliases like "ML", "Python programming"
   all resolve to one canonical skill name.
3. Use word-boundary matching (regex) so "R" doesn't match inside "Framework".
4. Return the canonical, de-duplicated list of detected skills.

This is intentionally dictionary-based (not a black-box ML model) so it is
transparent and easy to explain, extend, and debug. It can later be swapped
for a spaCy PhraseMatcher or a trained NER model without changing the
calling code, since the function signature stays the same.
"""
import re
from typing import List

# Master skill dictionary (canonical names).
# Add new skills here -- the rest of the pipeline picks them up automatically.
SKILL_DICTIONARY = [
    "Python", "Java", "JavaScript", "C++", "SQL", "Excel", "Pandas", "NumPy",
    "Scikit-learn", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning",
    "NLP", "React", "Node.js", "Django", "FastAPI", "AWS", "Azure", "Docker",
    "Git", "Power BI", "Tableau", "Statistics",
]

# Aliases / variants -> canonical skill name.
# Extend this as you discover more real-world phrasing in job descriptions.
NORMALIZATION_MAP = {
    "python3": "Python", "python 3": "Python", "python programming": "Python",
    "ml": "Machine Learning", "machine-learning": "Machine Learning",
    "dl": "Deep Learning",
    "js": "JavaScript",
    "nodejs": "Node.js", "node js": "Node.js",
    "sklearn": "Scikit-learn",
    "postgres": "SQL", "postgresql": "SQL", "mysql": "SQL",
    "power-bi": "Power BI", "powerbi": "Power BI",
    "amazon web services": "AWS",
    "microsoft azure": "Azure",
    "natural language processing": "NLP",
}


def _build_pattern(term: str) -> re.Pattern:
    """Whole-word, case-insensitive pattern for a (possibly multi-word) term."""
    escaped = re.escape(term)
    return re.compile(rf"(?<![A-Za-z0-9+#.]){escaped}(?![A-Za-z0-9+#])", re.IGNORECASE)


# Pre-compile patterns once at import time for speed.
_CANONICAL_PATTERNS = {skill: _build_pattern(skill) for skill in SKILL_DICTIONARY}
_ALIAS_PATTERNS = {alias: (_build_pattern(alias), canonical)
                    for alias, canonical in NORMALIZATION_MAP.items()}


def extract_skills(text: str) -> List[str]:
    """
    Detect known skills mentioned in `text`.
    Returns a sorted, de-duplicated list of canonical skill names.
    """
    if not text:
        return []

    found = set()

    for skill, pattern in _CANONICAL_PATTERNS.items():
        if pattern.search(text):
            found.add(skill)

    for alias, (pattern, canonical) in _ALIAS_PATTERNS.items():
        if pattern.search(text):
            found.add(canonical)

    return sorted(found)


def normalize_skill_name(raw: str) -> str:
    """Map a free-typed skill (e.g. user input 'ml') to its canonical name."""
    key = raw.strip().lower()
    if key in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[key]
    for skill in SKILL_DICTIONARY:
        if skill.lower() == key:
            return skill
    return raw.strip()
