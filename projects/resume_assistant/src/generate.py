"""Generation helpers: cover letters, interview questions, and reports."""

from __future__ import annotations

from typing import Any

from .llm import chat

_RECRUITER = "You are an expert technical recruiter."


def cover_letter(resume: str, job: str) -> str:
    """Generate a tailored cover letter for a resume/job pair.

    Args:
        resume: Raw resume text.
        job: Target job description text.

    Returns:
        A cover letter as plain text.
    """
    prompt = (
        "Write a concise, professional cover letter (3-4 short paragraphs) for "
        "the candidate below, tailored to the job description. Use a confident "
        "but genuine tone and highlight the most relevant strengths. Do not "
        "invent facts that are not supported by the resume.\n\n"
        f"=== RESUME ===\n{resume}\n\n=== JOB DESCRIPTION ===\n{job}\n"
    )
    return chat(prompt, system=_RECRUITER)


def interview_questions(job: str, n: int = 8) -> str:
    """Generate likely interview questions for a job description.

    Args:
        job: Target job description text.
        n: Number of questions to produce.

    Returns:
        A numbered list of questions as plain text.
    """
    prompt = (
        f"Generate {n} realistic interview questions for the following role. "
        "Mix technical and behavioural questions and number them.\n\n"
        f"=== JOB DESCRIPTION ===\n{job}\n"
    )
    return chat(prompt, system=_RECRUITER)


def report_md(a: dict[str, Any]) -> str:
    """Assemble a Markdown report from an :func:`~src.rag.analyze` result.

    Args:
        a: The analysis dict.

    Returns:
        A formatted Markdown document as a string.
    """
    matched = a.get("matched_skills") or []
    missing = a.get("missing_skills") or []
    bullets = a.get("bullet_suggestions") or []

    def _bullets(items: list) -> str:
        """Render a list as Markdown bullets, or a placeholder if empty."""
        return "\n".join(f"- {item}" for item in items) if items else "- _None_"

    return (
        "# 📄 AI Resume Assistant Report\n\n"
        f"## ATS Score: {a.get('ats_score', 0)}/100\n\n"
        "## Summary\n\n"
        f"{a.get('summary', '') or '_No summary available._'}\n\n"
        "## ✅ Matched Skills\n\n"
        f"{_bullets(matched)}\n\n"
        "## ❌ Missing Skills\n\n"
        f"{_bullets(missing)}\n\n"
        "## ✨ Suggested Resume Bullets\n\n"
        f"{_bullets(bullets)}\n\n"
        "---\n"
        "_Generated locally with Ollama — 100% private._\n"
    )
