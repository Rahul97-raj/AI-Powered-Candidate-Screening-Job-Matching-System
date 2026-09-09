import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.parser import extract_text
from src.llm import extract_resume, compare_resume_to_job
from src.scoring import calculate_match_score


load_dotenv()


st.set_page_config(
    page_title="AI Candidate Screening",
    page_icon="🧑‍💼",
    layout="wide",
)


st.title("🧑‍💼 AI-Powered Candidate Screening & Job Matching")

st.markdown(
    "Upload resumes, provide a job description, and get structured candidate "
    "profiles, skill gaps, match scores, and a ranked shortlist."
)


if not os.getenv("GROQ_API_KEY"):
    st.error(
        "GROQ_API_KEY is missing. Add it to `.env` and restart the app."
    )
    st.stop()


job_description = st.text_area(
    "1. Job Description",
    height=240,
    placeholder="Paste the complete job description and required skills...",
)


uploads = st.file_uploader(
    "2. Upload Candidate Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)


if st.button(
    "🚀 Screen Candidates",
    type="primary",
    use_container_width=True,
):

    if not job_description.strip():
        st.warning("Please enter a job description.")
        st.stop()

    if not uploads:
        st.warning("Please upload at least one PDF/DOCX resume.")
        st.stop()

    results = []
    progress = st.progress(0)

    for i, file in enumerate(uploads):

        try:
            # Extract text from PDF/DOCX
            text = extract_text(
                file.getvalue(),
                file.name
            )

            if not text.strip():
                st.warning(
                    f"No readable text found in {file.name}."
                )
                continue

            # Extract structured candidate information using LLM
            profile = extract_resume(text)

            # Compare candidate against job description
            comparison = compare_resume_to_job(
                profile,
                job_description
            )

            # Calculate deterministic skill-match score
            required_skills = comparison.matching_skills + comparison.missing_skills

            score_data = calculate_match_score(
                profile.skills,
                required_skills
            )

            score = score_data["match_percentage"]

            results.append(
                {
                    "filename": file.name,
                    "profile": profile,
                    "comparison": comparison,
                    "score": score,
                }
            )

        except Exception as exc:

            st.error(
                f"Could not process {file.name}: {exc}"
            )

        progress.progress(
            (i + 1) / len(uploads)
        )


    # Highest score first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    if not results:
        st.info(
            "No candidates could be processed."
        )
        st.stop()


    st.subheader("📊 Candidate Ranking")


    table = pd.DataFrame(
        [
            {
                "Rank": i + 1,
                "Candidate": r["filename"],
                "Match %": r["score"],
                "Matching Skills": len(
                    r["comparison"].matching_skills
                ),
                "Missing Skills": len(
                    r["comparison"].missing_skills
                ),
            }
            for i, r in enumerate(results)
        ]
    )


    st.dataframe(
        table,
        hide_index=True,
        use_container_width=True
    )


    st.divider()


    for rank, item in enumerate(
        results,
        1
    ):

        p = item["profile"]
        c = item["comparison"]

        with st.expander(
            f"#{rank}  {item['filename']} — "
            f"{item['score']}% Match",
            expanded=(rank == 1),
        ):

            a, b, d = st.columns(3)

            a.metric(
                "Match Score",
                f"{item['score']}%"
            )

            b.metric(
                "Matching Skills",
                len(c.matching_skills)
            )

            d.metric(
                "Missing Skills",
                len(c.missing_skills)
            )


            st.write(
                f"**Candidate:** "
                f"{p.name or 'Not specified'}"
            )

            st.write(
                f"**Email:** "
                f"{p.email or 'Not specified'}"
            )

            st.write(
                f"**Experience:** "
                f"{p.experience_summary or 'Not specified'}"
            )


            st.markdown("**Skills**")

            st.write(
                ", ".join(p.skills)
                or "None extracted"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.markdown(
                    "**✅ Matching Skills**"
                )

                st.write(
                    ", ".join(c.matching_skills)
                    or "None"
                )


            with col2:

                st.markdown(
                    "**❌ Missing Skills**"
                )

                st.write(
                    ", ".join(c.missing_skills)
                    or "None"
                )


            st.markdown(
                "**Recommendation**"
            )

            st.info(
                c.recommendation
                or "No recommendation returned."
            )


st.caption(
    "Portfolio/learning project — screening output "
    "should support, not replace, human hiring decisions."
)
