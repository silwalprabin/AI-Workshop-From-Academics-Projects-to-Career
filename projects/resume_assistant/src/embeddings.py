"""Embedding generation and a Chroma-backed vector index."""

from __future__ import annotations

import uuid

import chromadb
import requests

from .config import EMBED_MODEL, OLLAMA


def embed(text: str) -> list[float]:
    """Return the embedding vector for a piece of text via Ollama.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding.

    Raises:
        requests.HTTPError: If the Ollama server returns a non-2xx status.
    """
    r = requests.post(
        f"{OLLAMA}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["embedding"]


def build_index(chunks: list[str]):
    """Embed ``chunks`` and store them in a persistent Chroma collection.

    A fresh, uniquely-named set of ids is generated on every call and the
    "resume" collection is reset first so repeated analyses do not accumulate
    stale documents.

    Args:
        chunks: Text chunks to index.

    Returns:
        The populated Chroma collection object.
    """
    client = chromadb.PersistentClient(path=".chroma")

    # Start from a clean slate so a new resume fully replaces the previous one.
    try:
        client.delete_collection("resume")
    except Exception:  # noqa: BLE001 - collection may not exist yet
        pass

    col = client.get_or_create_collection("resume")

    if not chunks:
        return col

    ids = [str(uuid.uuid4()) for _ in chunks]
    embeddings = [embed(c) for c in chunks]
    col.add(ids=ids, embeddings=embeddings, documents=chunks)
    return col


def search(col, query: str, k: int = 4) -> list[str]:
    """Return the ``k`` most relevant documents for ``query``.

    Args:
        col: A Chroma collection produced by :func:`build_index`.
        query: The natural-language query (e.g. a job description).
        k: Number of documents to retrieve.

    Returns:
        A list of matching document strings (possibly fewer than ``k``).
    """
    result = col.query(query_embeddings=[embed(query)], n_results=k)
    documents = result.get("documents") or [[]]
    return documents[0]
