import json
import os
import re
from .text_cleaner import clean_text

def load_skills_db():
    """Load skills from JSON database"""
    skills_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'skills_db.json')
    try:
        with open(skills_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
        # Flatten all skills
        all_skills = []
        for category, skills in db.items():
            all_skills.extend(skills)
        return list(set(all_skills))  # unique
    except Exception as e:
        print(f"Error loading skills_db: {e}")
        return []

SKILLS_DB = load_skills_db()
print(f"Loaded {len(SKILLS_DB)} unique skills from skills_db.json")

def extract_skills(text):
    if not text:
        return []
    cleaned = clean_text(text)
    found_skills = []
    from fuzzywuzzy import fuzz
    for skill in SKILLS_DB:
        score = fuzz.partial_ratio(skill.lower(), cleaned)
        if score > 75:  # Fuzzy threshold
            found_skills.append(skill)
    # Remove duplicates, sort by score (implicit by order)
    found_skills = list(dict.fromkeys(found_skills))  # Preserve order, unique
    print(f"Extracted {len(found_skills)} skills (fuzzy): {found_skills[:10]}...")  # debug
    return found_skills
