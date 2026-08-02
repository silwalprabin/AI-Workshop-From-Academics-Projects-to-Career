"""Entry point for the GitHub Code Review Agent.

Usage:
    python main.py [<repo-url-or-local-path>]

The argument may be either a git URL to clone or an existing local directory to
review in place. When omitted it defaults to the bundled sample repository so
the workshop demo runs offline (apart from the local Ollama model).
"""

from __future__ import annotations

import os
import sys

from src.graph import app

# Default target: the tiny intentionally-imperfect sample repo shipped with the
# workshop. Resolved relative to this file so it works from any cwd.
_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO = os.path.normpath(
    os.path.join(_HERE, "..", "..", "datasets", "sample_repo")
)


def main() -> None:
    """Run the review graph against the requested repo and write review.md."""
    repo = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_REPO
    print(f"Reviewing: {repo}")

    # Seed the state; findings starts empty and is accumulated by the graph.
    result = app.invoke({"repo": repo, "findings": []})

    report = result.get("report", "# Code Review Report\n\nNo report generated.")
    out_path = os.path.join(_HERE, "review.md")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(report)

    print(f"Done. Report written to {out_path}")


if __name__ == "__main__":
    main()
