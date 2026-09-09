from src.models import JobComparison
from src.scoring import score_candidate


def test_full_skill_match():
    comparison = JobComparison(
        matching_skills=["Python", "SQL"],
        missing_skills=[],
        relevant_experience="Python internship",
        recommendation="Strong match",
    )
    assert score_candidate(comparison) == 100


def test_partial_match():
    comparison = JobComparison(
        matching_skills=["Python"],
        missing_skills=["SQL"],
        relevant_experience="Python project",
        recommendation="Good match",
    )
    assert score_candidate(comparison) == 65
