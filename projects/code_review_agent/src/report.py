"""Final report node: aggregates specialist findings into Markdown.

The :func:`reviewer` node groups every finding by the agent that produced it,
renders a Markdown document, and asks the LLM for a short overall summary and
severity assessment that is prepended to the report.
"""

from __future__ import annotations

from collections import defaultdict

from .llm import chat


def reviewer(state: dict) -> dict:
    """Group findings by specialist and build the final Markdown report.

    Args:
        state: The graph state, expected to contain ``repo`` and ``findings``.

    Returns:
        A dict with a single ``report`` key holding the Markdown string.
    """
    findings: list[dict] = state.get("findings", []) or []
    repo = state.get("repo", "unknown")

    # Gracefully handle the empty case -- no files or no issues found.
    if not findings:
        report = (
            f"# Code Review Report\n\n"
            f"**Repository:** `{repo}`\n\n"
            f"No findings were produced. Either the repository had no reviewable "
            f"files or the specialists reported no issues.\n"
        )
        return {"report": report}

    # Group findings by the agent that produced them.
    grouped: dict[str, list[dict]] = defaultdict(list)
    for f in findings:
        grouped[f.get("agent", "unknown")].append(f)

    # Build the per-specialist sections of the report.
    sections: list[str] = []
    for agent in sorted(grouped):
        sections.append(f"## {agent.capitalize()} review\n")
        for item in grouped[agent]:
            sections.append(f"### `{item.get('file', 'unknown')}`\n")
            sections.append(f"{item.get('note', '').strip()}\n")
    body = "\n".join(sections)

    # Ask the model for an executive summary + overall severity.
    try:
        summary = chat(
            "Summarize the following code review findings in 3-5 sentences and "
            "state an overall severity (low/med/high) with a one-line "
            "justification.\n\n" + body,
            system="You are a lead code reviewer writing an executive summary.",
        )
    except Exception as exc:  # never let summary failure lose the detailed body
        summary = f"_Summary unavailable ({exc})._"

    report = (
        f"# Code Review Report\n\n"
        f"**Repository:** `{repo}`\n\n"
        f"## Overall summary\n\n{summary.strip()}\n\n"
        f"---\n\n{body}"
    )
    return {"report": report}
