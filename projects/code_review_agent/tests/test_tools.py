"""Offline unit tests for the filesystem tools.

These tests never touch the network -- they only exercise ``list_files`` and
``read_file`` against a pytest ``tmp_path`` fixture.
"""

from __future__ import annotations

import os

from src.tools import list_files, read_file


def test_list_files_finds_python_files(tmp_path):
    """list_files should find .py files recursively and ignore others."""
    (tmp_path / "a.py").write_text("print('a')\n", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("not python\n", encoding="utf-8")
    sub = tmp_path / "pkg"
    sub.mkdir()
    (sub / "b.py").write_text("print('b')\n", encoding="utf-8")

    found = list_files(str(tmp_path), pattern="*.py")

    names = sorted(os.path.basename(p) for p in found)
    assert names == ["a.py", "b.py"]


def test_read_file_truncates_to_max_chars(tmp_path):
    """read_file should truncate content longer than max_chars."""
    big = tmp_path / "big.py"
    big.write_text("x" * 10_000, encoding="utf-8")

    out = read_file(str(big), max_chars=100)

    # The returned content is truncated to max_chars plus a marker.
    assert out.startswith("x" * 100)
    assert "[truncated]" in out
    assert len(out) < 10_000


def test_read_file_returns_full_content_when_short(tmp_path):
    """read_file should return the whole file when it is under the limit."""
    small = tmp_path / "small.py"
    small.write_text("hello", encoding="utf-8")

    assert read_file(str(small), max_chars=100) == "hello"
