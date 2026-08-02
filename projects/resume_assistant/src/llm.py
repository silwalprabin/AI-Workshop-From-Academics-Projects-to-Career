"""Thin client around the Ollama chat API plus small resilience helpers.

No network calls happen at import time; ``chat`` must be invoked explicitly.
"""

from __future__ import annotations

import json
import re
import time
from typing import Callable, Optional, TypeVar

import requests

from .config import LLM_MODEL, OLLAMA

T = TypeVar("T")


def chat(prompt: str, system: str = "") -> str:
    """Send a single-turn chat request to Ollama and return the reply text.

    Args:
        prompt: The user message.
        system: Optional system prompt that steers the model's behaviour.

    Returns:
        The assistant message content as a string.

    Raises:
        requests.HTTPError: If the Ollama server returns a non-2xx status.
        requests.RequestException: On connection/timeout errors.
    """
    r = requests.post(
        f"{OLLAMA}/api/chat",
        json={
            "model": LLM_MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]


def call_with_retry(fn: Callable[[], T], tries: int = 3) -> T:
    """Call ``fn`` up to ``tries`` times with exponential backoff.

    Args:
        fn: A zero-argument callable to invoke.
        tries: Maximum number of attempts before giving up.

    Returns:
        Whatever ``fn`` returns on its first successful call.

    Raises:
        Exception: Re-raises the last exception if all attempts fail.
    """
    last_exc: Optional[BaseException] = None
    for attempt in range(1, tries + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - deliberately broad for retry
            last_exc = exc
            if attempt < tries:
                # Exponential backoff: 1s, 2s, 4s, ...
                time.sleep(2 ** (attempt - 1))
    # If we get here every attempt failed; surface the final error.
    assert last_exc is not None
    raise last_exc


def safe_json(raw: str) -> Optional[dict]:
    """Best-effort parse of a JSON object from possibly-noisy LLM output.

    Strategy:
        1. Try ``json.loads`` directly.
        2. Otherwise extract the first ``{...}`` block and parse that.
        3. Otherwise return ``None`` (never raises).

    Args:
        raw: Raw text returned by the model.

    Returns:
        A parsed ``dict`` or ``None`` when nothing usable was found.
    """
    if not raw:
        return None

    # 1. Straight parse.
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else None
    except (json.JSONDecodeError, TypeError):
        pass

    # 2. Extract the first balanced-ish {...} block (greedy to the last brace).
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None

    # 3. Nothing worked.
    return None
