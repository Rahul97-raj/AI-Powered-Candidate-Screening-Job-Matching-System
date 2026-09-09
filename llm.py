import json
import os

from groq import Groq
from .models import CandidateProfile, JobComparison


MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "phone": {"type": "string"},
        "skills": {"type": "array", "items": {"type": "string"}},
        "experience_summary": {"type": "string"},
        "education": {"type": "array", "items": {"type": "string"}},
        "projects": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "name", "email", "phone", "skills",
        "experience_summary", "education", "projects"
    ],
    "additionalProperties": False,
}

COMPARISON_SCHEMA = {
    "type": "object",
    "properties": {
        "matching_skills": {"type": "array", "items": {"type": "string"}},
        "missing_skills": {"type": "array", "items": {"type": "string"}},
        "relevant_experience": {"type": "string"},
        "recommendation": {"type": "string"},
    },
    "required": [
        "matching_skills", "missing_skills",
        "relevant_experience", "recommendation"
    ],
    "additionalProperties": False,
}


def _json_completion(system_prompt: str, user_prompt: str, name: str, schema: dict):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": name,
                "strict": True,
                "schema": schema,
            },
        },
    )
    return json.loads(response.choices[0].message.content)


def extract_resume(resume_text: str) -> CandidateProfile:
    data = _json_completion(
        """Extract structured information from a resume.
Do not invent facts. Use empty strings/lists when information is unavailable.""",
        resume_text,
        "candidate_profile",
        PROFILE_SCHEMA,
    )
    return CandidateProfile.model_validate(data)


def compare_resume_to_job(profile: CandidateProfile, job_description: str) -> JobComparison:
    prompt = f"""Compare the candidate against the job description.

Candidate profile:
{profile.model_dump_json(indent=2)}

Job description:
{job_description}

Normalize obvious case/spelling variations. Mark a skill as matching only
when there is evidence in the candidate profile. Identify missing required
skills and summarize relevant experience."""
    data = _json_completion(
        "You are an objective candidate-matching assistant. Do not use protected characteristics.",
        prompt,
        "job_comparison",
        COMPARISON_SCHEMA,
    )
    return JobComparison.model_validate(data)
