"""Filesystem and git helper tools used by the review graph.

These are deliberately dependency-light so they can be unit tested without any
network access.
"""

from __future__ import annotations

import fnmatch
import os
import shutil
import subprocess


def clone_repo(url: str, dest: str = ".repo") -> str:
    """Shallow-clone a git repository into ``dest``.

    If ``dest`` already exists it is removed first so the clone starts from a
    clean state. Uses ``--depth 1`` because we only ever inspect the current
    tree, never history.

    Args:
        url: The git clone URL (https or ssh).
        dest: Target directory for the clone.

    Returns:
        The path to the cloned working tree (``dest``).

    Raises:
        subprocess.CalledProcessError: If ``git clone`` exits non-zero.
    """
    # Start from a clean directory so repeated runs are deterministic.
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)

    subprocess.run(
        ["git", "clone", "--depth", "1", url, dest],
        check=True,
    )
    return dest


def list_files(root: str, pattern: str = "*.py") -> list[str]:
    """Recursively list files under ``root`` matching a glob ``pattern``.

    Args:
        root: Directory to walk.
        pattern: ``fnmatch`` style glob (e.g. ``"*.py"``).

    Returns:
        A sorted list of matching file paths.
    """
    matches: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if fnmatch.fnmatch(name, pattern):
                matches.append(os.path.join(dirpath, name))
    return sorted(matches)


def read_file(path: str, max_chars: int = 6000) -> str:
    """Read a text file, ignoring decode errors, truncated to ``max_chars``.

    Args:
        path: Path to the file to read.
        max_chars: Maximum number of characters to return.

    Returns:
        The (possibly truncated) file contents. Truncation appends a marker.
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read()
    if len(content) > max_chars:
        return content[:max_chars] + "\n... [truncated]"
    return content
