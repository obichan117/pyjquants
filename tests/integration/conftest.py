"""Conftest for integration tests.

Integration tests require a real J-Quants API key.
Set JQUANTS_API_KEY in .env or environment.

Run integration tests:
    uv run pytest tests/integration/ -v

Skip integration tests (default in CI):
    uv run pytest tests/ --ignore=tests/integration/
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest


def load_dotenv() -> None:
    """Load .env file into environment variables."""
    env_file = Path(__file__).parent.parent.parent / ".env"
    if not env_file.exists():
        return

    with open(env_file) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Parse key=value (handle values with = in them)
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                # Remove surrounding quotes if present
                if value and value[0] in ('"', "'") and value[-1] == value[0]:
                    value = value[1:-1]
                # Only set if not already in environment
                if key and key not in os.environ:
                    os.environ[key] = value


# Load .env at module import time
load_dotenv()


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test (requires API key)",
    )
    config.addinivalue_line(
        "markers",
        "standard_tier: mark test as requiring Standard+ tier",
    )


@pytest.fixture(scope="session")
def api_key() -> str:
    """Get API key, skip if not available."""
    key = os.environ.get("JQUANTS_API_KEY")
    if not key or key == "your_api_key_here":
        pytest.skip("JQUANTS_API_KEY not set. Copy .env.example to .env and add your key.")
    return key


@pytest.fixture(scope="session")
def is_standard_tier() -> bool:
    """Check if user has Standard+ tier based on rate limit setting."""
    rate_limit = int(os.environ.get("JQUANTS_RATE_LIMIT", "60"))
    return rate_limit >= 120


def skip_if_not_standard(is_standard_tier: bool) -> None:
    """Skip test if not on Standard+ tier."""
    if not is_standard_tier:
        pytest.skip("Requires Standard+ tier (set JQUANTS_RATE_LIMIT=120 or higher)")
