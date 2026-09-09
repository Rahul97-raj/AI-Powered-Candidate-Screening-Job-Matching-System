# AI-Powered Candidate Screening & Job Matching System

> An LLM-powered resume screening application that extracts structured candidate information from PDF/DOCX resumes and compares candidates against job requirements.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic-red)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)

## Overview

Recruiters often need to review many resumes against the same job description. This project automates the repetitive first-pass analysis:

**Resume → Text Extraction → LLM Structuring → Pydantic Validation → Job Matching → Skill Gap Analysis → Score → Ranking**

The application accepts multiple PDF/DOCX resumes, extracts candidate details using an LLM, compares those details with a job description, and presents an interpretable shortlist.

## Features

- Upload multiple **PDF/DOCX resumes**
- Extract resume text using `pypdf` and `python-docx`
- Extract structured candidate data using a Groq-hosted LLM
- Validate the LLM output with **Pydantic schemas**
- Identify:
  - Skills
  - Experience
  - Education
  - Projects
- Compare candidates with job requirements
- Identify **matching skills**
- Identify **missing skills**
- Calculate a transparent match percentage
- Rank multiple candidates
- Streamlit dashboard for interactive screening

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Groq API | LLM inference |
| LLM | Resume extraction and candidate/JD comparison |
| Pydantic | Structured output validation |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| Streamlit | Web interface |
| Pandas | Ranking table |

## Architecture

```text
                 ┌──────────────────────┐
                 │ PDF / DOCX Resumes   │
                 └──────────┬───────────┘
                            │
                ┌───────────▼───────────┐
                │ Text Extraction       │
                │ pypdf / python-docx   │
                └───────────┬───────────┘
                            │
                ┌───────────▼───────────┐
                │ Groq LLM               │
                │ Structured Extraction  │
                └───────────┬───────────┘
                            │
                ┌───────────▼───────────┐
                │ Pydantic Schema        │
                │ CandidateProfile       │
                └───────────┬───────────┘
                            │
                            ▼
               Skills / Experience /
               Education / Projects
                            │
                            │
          ┌─────────────────▼─────────────────┐
          │          Job Description           │
          └─────────────────┬─────────────────┘
                            │
                ┌───────────▼───────────┐
                │ LLM Comparison         │
                └───────────┬───────────┘
                            │
               ┌────────────┼────────────┐
               ▼            ▼            ▼
          Matching       Missing      Relevant
           Skills         Skills      Experience
               └────────────┼────────────┘
                            ▼
                   Transparent Score
                            │
                            ▼
                    Candidate Ranking
```

## Project Structure

```text
AI-Powered-Candidate-Screening-Job-Matching-System/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── parser.py
│   ├── models.py
│   ├── llm.py
│   └── scoring.py
│
├── sample_data/
│   ├── job_description.txt
│   └── sample_resume.txt
│
├── docs/
│   └── architecture.md
│
└── tests/
    └── test_scoring.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Powered-Candidate-Screening-Job-Matching-System.git
cd AI-Powered-Candidate-Screening-Job-Matching-System
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Groq

Copy `.env.example` to `.env` and add your own API key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

**Never commit `.env` or an API key to GitHub.**

### 5. Run

```bash
streamlit run app.py
```

The application will open in your browser.

## How the Matching Works

The system first extracts the resume into a structured `CandidateProfile`.

Then it compares the candidate profile with the job description and produces:

- `matching_skills`
- `missing_skills`
- `relevant_experience`
- `recommendation`

The final score is intentionally transparent:

```text
Skill Coverage = Matching Skills / (Matching + Missing Skills)

Final Score =
    70% × Skill Coverage
  + 30% × Relevant Experience Signal
```

This makes the ranking logic easy to understand and explain rather than hiding the score inside an opaque model.

## Example

For a Python/AI internship, a candidate might produce:

```text
Match Score: 82%

Matching Skills:
- Python
- SQL
- Pandas
- NumPy
- Pydantic
- LLM APIs

Missing Skills:
- REST APIs
- Basic Machine Learning

Relevant Experience:
Candidate has experience building Python and LLM-based projects.

Recommendation:
Strong match with some gaps in the required skill set.
```

## Engineering Decisions

### Why Pydantic?

LLMs can return inconsistent structures. Pydantic provides a typed contract for candidate information and validates the returned data before the application uses it.

### Why separate parsing and LLM modules?

File parsing is deterministic, while information extraction is probabilistic. Keeping them separate makes the code easier to test and replace.

### Why a deterministic scoring layer?

The LLM identifies the evidence and skill gaps, while a small deterministic function calculates the final percentage. This makes the score explainable and reproducible.

## Limitations

- Scanned/image-only PDFs require OCR, which is not included.
- Skill matching is based on extracted text and LLM interpretation.
- The score is a portfolio-oriented heuristic, not a validated hiring metric.
- LLM/API failures need retry handling in a production deployment.
- Candidate screening should support human review rather than make autonomous employment decisions.

## Future Improvements

- OCR for scanned resumes
- Batch processing with persistent storage
- Embedding-based semantic skill matching
- Recruiter authentication
- Export ranked candidates to CSV
- Evaluation dataset and automated accuracy tests
- Caching and retry/backoff for production API usage
- Explainable evidence snippets for each matched skill

## Interview Explanation

A concise way to explain the project:

> "I built an LLM-based candidate screening system where I first extract text from PDF and DOCX resumes using pypdf and python-docx. I send the unstructured resume text to a Groq-hosted LLM and constrain the response with a Pydantic schema so I get structured fields like skills, experience, education and projects. Then I compare that structured profile against a job description to identify matching and missing skills. Finally, I use a deterministic scoring function to calculate a match percentage and rank multiple candidates. I kept the scoring layer separate from the LLM so the final ranking is more transparent and explainable."

## Disclaimer

This repository is a portfolio/learning implementation. It is not intended to make autonomous employment decisions or evaluate protected characteristics.
