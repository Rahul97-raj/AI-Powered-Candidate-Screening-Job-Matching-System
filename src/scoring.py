from typing import List, Dict


def calculate_match_score(
    candidate_skills: List[str],
    required_skills: List[str]
) -> Dict:

    candidate = {
        skill.strip().lower()
        for skill in candidate_skills
        if skill.strip()
    }

    required = {
        skill.strip().lower()
        for skill in required_skills
        if skill.strip()
    }

    if not required:
        return {
            "match_percentage": 0.0,
            "matching_skills": [],
            "missing_skills": []
        }

    matching = sorted(candidate.intersection(required))
    missing = sorted(required.difference(candidate))

    percentage = (len(matching) / len(required)) * 100

    return {
        "match_percentage": round(percentage, 2),
        "matching_skills": matching,
        "missing_skills": missing
    }
