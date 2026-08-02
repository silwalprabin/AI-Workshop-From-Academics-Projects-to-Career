# Sample Repo (intentionally imperfect)

A tiny Python project used as review material for the **GitHub Code Review
Agent** workshop. It deliberately contains realistic problems for the agents to
find:

- **Security** — a hardcoded API key / password in `config.py`, and a secret
  printed to stdout in `app.py`.
- **Performance** — O(n·m) nested loops in `analytics.py` and a repeated linear
  scan in `data_loader.py`.
- **Documentation** — missing docstrings and type hints across all modules.
- **Robustness / testing** — `average()` divides by zero on an empty list and
  `load_json()` has no error handling; there are **no tests** at all.

Files:

| File             | What it does                                  |
| ---------------- | --------------------------------------------- |
| `config.py`      | App config (with hardcoded secrets)           |
| `analytics.py`   | User/number helpers (with inefficient loops)  |
| `data_loader.py` | JSON loading + record lookup                  |
| `app.py`         | Entry point wiring it all together            |

> This code is intentionally flawed for teaching purposes. Do not use it as a
> reference for good practice.
