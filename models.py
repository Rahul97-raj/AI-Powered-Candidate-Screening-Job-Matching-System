from typing import List
from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    skills: List[str] = Field(default_factory=list)
    experience_summary: str = ""
    education: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)


class JobComparison(BaseModel):
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    relevant_experience: str = ""
    recommendation: str = ""
