"""Minimal GitHub REST API helpers.

Used to fetch repository metadata and (optionally) post a review as an issue
comment. Authentication uses a Bearer token read from configuration -- tokens
are never hard-coded.
"""

from __future__ import annotations

import requests

from .config import GITHUB_TOKEN

_API = "https://api.github.com"


def _headers() -> dict[str, str]:
    """Build request headers, adding the Bearer token only if configured."""
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def repo_meta(owner: str, repo: str) -> dict:
    """Fetch repository metadata from the GitHub API.

    Args:
        owner: The repository owner (user or org).
        repo: The repository name.

    Returns:
        The parsed JSON metadata for the repository.

    Raises:
        requests.HTTPError: If the request fails.
    """
    r = requests.get(f"{_API}/repos/{owner}/{repo}", headers=_headers(), timeout=30)
    r.raise_for_status()
    return r.json()


def post_comment(owner: str, repo: str, issue: int, body: str) -> dict:
    """Post a comment on an issue or pull request.

    Args:
        owner: The repository owner.
        repo: The repository name.
        issue: The issue or pull request number.
        body: The Markdown comment body.

    Returns:
        The parsed JSON of the created comment.

    Raises:
        requests.HTTPError: If the request fails.
    """
    r = requests.post(
        f"{_API}/repos/{owner}/{repo}/issues/{issue}/comments",
        headers=_headers(),
        json={"body": body},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()
