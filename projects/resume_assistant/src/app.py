"""Streamlit UI for the AI Resume Assistant.

Run with:
    streamlit run src/app.py
"""

from __future__ import annotations

import tempfile

import streamlit as st

from src.embeddings import build_index
from src.generate import cover_letter, interview_questions, report_md
from src.ingest import chunk, read_pdf
from src.rag import analyze

OLLAMA_NOTE = (
    "Make sure Ollama is running locally and the models are pulled:\n\n"
    "```\nollama pull llama3.2\nollama pull nomic-embed-text\n```"
)


@st.cache_resource(show_spinner=False)
def _index_resume(resume_text: str):
    """Build (and cache) a vector index for a given resume text.

    Streamlit caches on the argument value, so re-running with the same resume
    text avoids re-embedding every chunk.
    """
    return build_index(chunk(resume_text))


def main() -> None:
    """Render the Streamlit application."""
    st.set_page_config(page_title="AI Resume Assistant", page_icon="📄")
    st.title("📄 AI Resume Assistant")
    st.caption("Local, private resume analysis powered by Ollama + RAG.")

    uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    job = st.text_area("Paste the job description", height=200)

    if st.button("Analyze", type="primary"):
        if uploaded is None:
            st.warning("Please upload a resume PDF first.")
            return
        if not job.strip():
            st.warning("Please paste a job description first.")
            return

        try:
            # Persist the upload to a temp file so pypdf can read it by path.
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".pdf"
            ) as tmp:
                tmp.write(uploaded.getvalue())
                tmp_path = tmp.name

            with st.spinner("Reading resume..."):
                resume_text = read_pdf(tmp_path)

            if len(resume_text.strip()) < 20:
                st.error(
                    "Could not extract text from this PDF. It may be a scanned "
                    "image. Please upload a text-based PDF."
                )
                return

            with st.spinner("Indexing and analyzing (this calls Ollama)..."):
                col = _index_resume(resume_text)
                a = analyze(col, job)

            # --- Results -------------------------------------------------
            st.metric("ATS Score", f"{a['ats_score']}/100")
            st.write(a.get("summary", ""))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Matched Skills")
                for skill in a.get("matched_skills", []):
                    st.write(f"- {skill}")
            with col2:
                st.subheader("❌ Missing Skills")
                for skill in a.get("missing_skills", []):
                    st.write(f"- {skill}")

            st.subheader("✨ Suggested Resume Bullets")
            for bullet in a.get("bullet_suggestions", []):
                st.write(f"- {bullet}")

            with st.spinner("Drafting cover letter..."):
                letter = cover_letter(resume_text, job)
            st.subheader("✉️ Cover Letter")
            st.write(letter)

            with st.spinner("Preparing interview questions..."):
                questions = interview_questions(job)
            st.subheader("🎤 Interview Questions")
            st.write(questions)

            # Downloadable Markdown report.
            st.download_button(
                "⬇️ Download Report (Markdown)",
                data=report_md(a),
                file_name="resume_report.md",
                mime="text/markdown",
            )

        except Exception as exc:  # noqa: BLE001 - surface any failure in the UI
            st.error(f"Something went wrong: {exc}")
            st.info(OLLAMA_NOTE)


if __name__ == "__main__":
    main()
