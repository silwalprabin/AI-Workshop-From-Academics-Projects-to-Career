"""Tests for the ingestion utilities (no Ollama required)."""

from __future__ import annotations

import os

from src.ingest import chunk, read_pdf

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SAMPLE_PDF = os.path.abspath(os.path.join(DATA_DIR, "sample_resume.pdf"))


def test_read_pdf_returns_text() -> None:
    """read_pdf should extract a meaningful amount of text."""
    text = read_pdf(SAMPLE_PDF)
    assert isinstance(text, str)
    assert len(text) > 100


def test_chunk_returns_non_empty_strings() -> None:
    """chunk should return a non-empty list of non-empty strings."""
    text = read_pdf(SAMPLE_PDF)
    chunks = chunk(text)
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert all(isinstance(c, str) and c.strip() for c in chunks)


def test_chunk_empty_input() -> None:
    """chunk on empty text returns an empty list."""
    assert chunk("") == []
