"""LangGraph wiring for the multi-agent code review workflow.

The graph fans out from a single clone/list node to one node per review
specialty, then fans back in to a single reviewer node that produces the report:

    START -> clone -> {security, performance, docs, testing} -> reviewer -> END
"""

from __future__ import annotations

import os

from langgraph.graph import END, START, StateGraph

from .agents import ReviewState, specialist
from .report import reviewer
from .rubrics import SPECIALISTS
from .tools import clone_repo, list_files


def clone_node(state: ReviewState) -> dict:
    """Resolve the repo to a local path and list its Python files.

    If ``repo`` is an existing local directory we review it in place; otherwise
    it is treated as a git URL and shallow-cloned first.

    Args:
        state: The graph state containing the ``repo`` value.

    Returns:
        A dict with the discovered ``files`` list.
    """
    repo = state["repo"]
    if os.path.isdir(repo):
        # Local path -- review it directly, no cloning needed.
        root = repo
    else:
        # Remote URL -- shallow clone into the default ".repo" directory.
        root = clone_repo(repo)
    files = list_files(root, pattern="*.py")
    return {"files": files}


def build_graph():
    """Construct and compile the review StateGraph."""
    g = StateGraph(ReviewState)

    # Entry node that produces the file list.
    g.add_node("clone", clone_node)

    # One specialist node per rubric, built by the factory.
    for name, rubric in SPECIALISTS.items():
        g.add_node(name, specialist(name, rubric))

    # Aggregation / report node.
    g.add_node("reviewer", reviewer)

    # Wire the edges: START -> clone -> fan-out -> fan-in -> reviewer -> END.
    g.add_edge(START, "clone")
    for name in SPECIALISTS:
        g.add_edge("clone", name)      # fan-out
        g.add_edge(name, "reviewer")   # fan-in
    g.add_edge("reviewer", END)

    return g.compile()


# Compiled application graph imported by main.py. Building the graph performs no
# network calls, so this is safe at import time.
app = build_graph()
