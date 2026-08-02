"""Configuration module.

Loads environment variables from a local ``.env`` file (via python-dotenv)
and exposes them as module-level constants. Importing this module performs
NO network calls, so it is safe to import even when Ollama is not running.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

# Load variables from a `.env` file into the process environment (if present).
# This is a no-op when the file is missing, so it is safe in every environment.
load_dotenv()

# Base URL of the local Ollama server.
OLLAMA: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Chat / generation model served by Ollama.
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2")

# Embedding model served by Ollama.
EMBED_MODEL: str = os.getenv("EMBED_MODEL", "nomic-embed-text")
