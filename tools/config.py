"""Shared configuration for tools.

Loads environment variables from `.env` and exposes project paths so every
tool resolves secrets and the .tmp directory the same way. Import this at the
top of any tool script:

    from config import env, TMP_DIR
    api_key = env("ANTHROPIC_API_KEY")
"""
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "python-dotenv is not installed. Run: pip install -r requirements.txt"
    ) from exc

# Project root is the parent of this tools/ directory.
ROOT_DIR = Path(__file__).resolve().parent.parent
TMP_DIR = ROOT_DIR / ".tmp"
WORKFLOWS_DIR = ROOT_DIR / "workflows"

# Load .env from the project root.
load_dotenv(ROOT_DIR / ".env")

# Ensure the temp directory exists for intermediate files.
TMP_DIR.mkdir(exist_ok=True)


def env(key: str, default: str | None = None, *, required: bool = False) -> str | None:
    """Read an environment variable.

    Set required=True to fail fast with a clear message when a secret is missing.
    """
    value = os.getenv(key, default)
    if required and not value:
        raise SystemExit(
            f"Missing required environment variable '{key}'. "
            f"Add it to {ROOT_DIR / '.env'} (see .env.example)."
        )
    return value
