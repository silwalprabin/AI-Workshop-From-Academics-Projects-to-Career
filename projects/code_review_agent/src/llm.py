"""Thin client for talking to a local Ollama chat model.

Exposes a single :func:`chat` helper used by every reviewer agent. A small retry
wrapper guards against transient connection hiccups with the local daemon.
"""

from __future__ import annotations

import time

import requests

from .config import LLM_MODEL, OLLAMA


def _post_chat(prompt: str, system: str, timeout: int) -> str:
    """Perform a single (non-streaming) chat request against Ollama.

    Args:
        prompt: The user message content.
        system: An optional system prompt establishing the agent persona.
        timeout: Per-request timeout in seconds.

    Returns:
        The assistant message content returned by the model.
    """
    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    r = requests.post(
        f"{OLLAMA}/api/chat",
        json={"model": LLM_MODEL, "stream": False, "messages": messages},
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]


def chat(prompt: str, system: str = "", *, retries: int = 3, timeout: int = 120) -> str:
    """Send a prompt to the local Ollama model and return the reply text.

    Retries a handful of times with linear backoff so a momentarily busy or
    just-started daemon does not fail the whole review run.

    Args:
        prompt: The user message content.
        system: Optional system prompt (agent persona / instructions).
        retries: Number of attempts before giving up.
        timeout: Per-request timeout in seconds.

    Returns:
        The model's response content.

    Raises:
        requests.RequestException: If every attempt fails.
    """
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return _post_chat(prompt, system, timeout)
        except requests.RequestException as exc:  # network / HTTP errors
            last_error = exc
            if attempt < retries:
                # Linear backoff: 1s, 2s, 3s ...
                time.sleep(attempt)
    # Exhausted all retries -- surface the last error to the caller.
    assert last_error is not None
    raise last_error
