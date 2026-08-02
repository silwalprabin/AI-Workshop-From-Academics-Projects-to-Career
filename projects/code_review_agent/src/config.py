"""Configuration loader for the GitHub Code Review Agent.

Loads environment variables from a local ``.env`` file (if present) and exposes
the handful of settings the rest of the application relies on. No network calls
happen at import time -- this module only reads configuration.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

# Load variables from a .env file into the process environment (no-op if absent).
load_dotenv()

# Base URL of the running Ollama server. Defaults to the local daemon.
OLLAMA: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Name of the local model served by Ollama that we ask to perform reviews.
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2")

# Optional GitHub personal access token. May be None when not configured;
# used only for authenticated GitHub API calls. Never hard-code this value.
GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN")
