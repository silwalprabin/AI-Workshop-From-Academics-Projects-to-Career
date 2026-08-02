"""Specialist reviewer agents and the shared graph state.

Each specialist is produced by the :func:`specialist` factory, which binds a
name and a rubric into a LangGraph node function. Nodes read the first handful
of files in the repo, ask the local model to review each one, and append their
findings to the shared state.
"""

from __future__ import annotations

import operator
from typing import Annotated, Callable, TypedDict

from .llm import chat
from .tools import read_file

# Only review the first N files so a large repo does not blow up the demo.
MAX_FILES: int = 8


class ReviewState(TypedDict):
    """Shared state passed between nodes of the review graph.

    Attributes:
        repo: The repo URL or local path being reviewed.
        files: Paths of the source files to review.
        findings: Accumulated findings; ``operator.add`` merges the lists
            returned by each specialist during the fan-out.
        report: The final Markdown report produced by the reviewer node.
    """

    repo: str
    files: list[str]
    findings: Annotated[list, operator.add]
    report: str


def specialist(name: str, rubric: str) -> Callable[[ReviewState], dict]:
    """Build a LangGraph node function for a single review specialty.

    Args:
        name: The specialist's name (e.g. ``"security"``).
        rubric: The review prompt describing what to look for and the output
            format.

    Returns:
        A node function ``node(state) -> dict`` suitable for ``add_node``.
    """

    def node(state: ReviewState) -> dict:
        """Review up to ``MAX_FILES`` files and return this agent's findings."""
        notes: list[dict[str, str]] = []
        for path in state["files"][:MAX_FILES]:
            content = read_file(path)
            prompt = f"{rubric}\n\n# File: {path}\n```python\n{content}\n```"
            try:
                feedback = chat(prompt, system=f"You are a {name} reviewer.")
            except Exception as exc:  # keep the graph alive on a single failure
                feedback = f"[error contacting model: {exc}]"
            notes.append({"agent": name, "file": path, "note": feedback})
        # Returning only the "findings" key -- operator.add merges it into state.
        return {"findings": notes}

    return node
