# Architecture Notes

## Pipeline

1. `app.py` receives a job description and uploaded resumes.
2. `parser.py` detects PDF/DOCX and extracts text.
3. `llm.py` sends resume text to Groq and requests structured JSON.
4. `models.py` validates the response with Pydantic.
5. The candidate profile is compared with the job description.
6. `scoring.py` calculates a deterministic percentage.
7. `app.py` sorts candidates and renders the ranking.

## Separation of Responsibilities

- **Parsing:** file-to-text conversion
- **LLM:** unstructured text understanding and comparison
- **Models:** data contract/validation
- **Scoring:** deterministic business logic
- **UI:** input, output, ranking and visualization

This separation makes the project easier to debug, test and extend.
