"""Optional FastAPI service exposing the analysis pipeline.

Run with:
    uvicorn src.api:app --reload
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from .rag import analyze_text

app = FastAPI(title="AI Resume Assistant API")


class Req(BaseModel):
    """Request body for the /analyze endpoint."""

    resume: str
    job: str


@app.get("/health")
def health() -> dict[str, str]:
    """Simple liveness probe."""
    return {"status": "ok"}


@app.post("/analyze")
def analyze_endpoint(req: Req) -> dict[str, Any]:
    """Analyse a resume string against a job description.

    Args:
        req: The request body with ``resume`` and ``job`` text.

    Returns:
        The structured analysis dict.
    """
    return analyze_text(req.resume, req.job)
