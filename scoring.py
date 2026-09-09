def score_candidate(comparison) -> int:
    """Calculate a transparent score from skill coverage and relevant experience."""
    total_skills = len(comparison.matching_skills) + len(comparison.missing_skills)
    skill_score = (
        len(comparison.matching_skills) / total_skills
        if total_skills else 0
    )
    experience_score = 1 if comparison.relevant_experience.strip() else 0

    # 70% skill coverage + 30% relevant-experience signal.
    return round((skill_score * 0.70 + experience_score * 0.30) * 100)
