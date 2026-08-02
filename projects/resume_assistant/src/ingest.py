"""PDF ingestion and text chunking utilities."""

from __future__ import annotations

from pypdf import PdfReader


def read_pdf(path: str) -> str:
    """Extract all text from a PDF file.

    Args:
        path: Filesystem path to a PDF document.

    Returns:
        The concatenated text of every page, separated by newlines.
    """
    reader = PdfReader(path)
    pages: list[str] = []
    for page in reader.pages:
        # ``extract_text`` can return ``None`` for image-only pages.
        pages.append(page.extract_text() or "")
    return "\n".join(pages)


def chunk(text: str, size: int = 500, overlap: int = 80) -> list[str]:
    """Split text into overlapping word windows.

    Args:
        text: The source text to split.
        size: Target window size, in words.
        overlap: Number of words shared between consecutive windows.

    Returns:
        A list of chunk strings (empty list for empty input).
    """
    words = text.split()
    if not words:
        return []

    # ``step`` must be positive even if the caller passes a large overlap.
    step = max(1, size - overlap)
    chunks: list[str] = []
    for start in range(0, len(words), step):
        window = words[start : start + size]
        if window:
            chunks.append(" ".join(window))
        # Stop once we have consumed the final word.
        if start + size >= len(words):
            break
    return chunks
