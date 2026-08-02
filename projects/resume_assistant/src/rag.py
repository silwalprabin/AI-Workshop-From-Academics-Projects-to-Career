"""Retrieval-augmented resume analysis pipeline."""

from __future__ import annotations

from typing import Any

from .embeddings import build_index, search
from .ingest import chunk
from .llm import chat, safe_json

SYSTEM = "You are an expert technical recruiter."

# Instruct the model to answer with a strict JSON schema so we can parse it.
_PROMPT_TEMPLATE = """\
Compare the candidate's resume against the job description and produce a
structured analysis.

Return ONLY a JSON object (no markdown, no commentary) with exactly these keys:
- "ats_score": integer 0-100 estimating how well the resume matches the job.
- "matched_skills": array of strings the resume already demonstrates.
- "missing_skills": array of strings the job wants but the resume lacks.
- "bullet_suggestions": array of strings, improved resume bullet points.
- "summary": a short string summarising the fit.

=== RESUME CONTEXT (most relevant excerpts) ===
{context}

=== JOB DESCRIPTION ===
{job}
"""

# Default structure returned when the model output is unusable.
_FALLBACK: dict[str, Any] = {
    "ats_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "bullet_suggestions": [],
    "summary": "Unable to parse a structured analysis from the model output.",
}


def _normalize(data: dict[str, Any]) -> dict[str, Any]:
    """Coerce a parsed dict into the expected schema with safe defaults."""
    result = dict(_FALLBACK)
    result.update({k: v for k, v in data.items() if k in _FALLBACK})

    # Clamp the score into 0-100 and force it to an int when possible.
    try:
        score = int(result["ats_score"])
    except (TypeError, ValueError):
        score = 0
    result["ats_score"] = max(0, min(100, score))

    # Guarantee list-typed fields are lists.
    for key in ("matched_skills", "missing_skills", "bullet_suggestions"):
        if not isinstance(result[key], list):
            result[key] = [result[key]] if result[key] else []

    result["summary"] = str(result.get("summary", ""))
    return result


def analyze(col, job_desc: str) -> dict[str, Any]:
    """Analyse a resume (indexed in ``col``) against a job description.

    Retrieves the most relevant resume excerpts, asks the LLM for a JSON
    analysis, and parses it defensively (retrying once on parse failure).

    Args:
        col: A Chroma collection produced by :func:`build_index`.
        job_desc: The target job description text.

    Returns:
        A dict with keys ``ats_score``, ``matched_skills``, ``missing_skills``,
        ``bullet_suggestions`` and ``summary``. Never raises on bad LLM output.
    """
    context_chunks = search(col, job_desc, k=4)
    context = "\n---\n".join(context_chunks) if context_chunks else "(no context)"
    prompt = _PROMPT_TEMPLATE.format(context=context, job=job_desc)

    raw = chat(prompt, system=SYSTEM)
    parsed = safe_json(raw)

    # Retry once with a firmer instruction if the first attempt failed to parse.
    if parsed is None:
        raw = chat(
            prompt + "\n\nReturn valid JSON only. Do not include any prose.",
            system=SYSTEM,
        )
        parsed = safe_json(raw)

    if parsed is None:
        return dict(_FALLBACK)

    return _normalize(parsed)


def analyze_text(resume: str, job: str) -> dict[str, Any]:
    """Convenience wrapper: chunk + index a resume string, then analyse it.

    Used by the optional FastAPI endpoint.

    Args:
        resume: Raw resume text.
        job: Target job description text.

    Returns:
        The analysis dict from :func:`analyze`.
    """
    col = build_index(chunk(resume))
    return analyze(col, job)
