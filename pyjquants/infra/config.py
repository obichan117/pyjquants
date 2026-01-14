"""Configuration loading from environment variables and TOML files."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

# Try to import tomllib (Python 3.11+) or tomli
_tomllib: ModuleType | None = None
if sys.version_info >= (3, 11):
    import tomllib

    _tomllib = tomllib
else:
    try:
        import tomli as _tomli_module

        _tomllib = _tomli_module
    except ImportError:
        pass


@dataclass
class JQuantsConfig:
    """Configuration for J-Quants API (V2).

    V2 uses API key authentication instead of email/password token flow.
    Get your API key from the J-Quants dashboard.
    """

    api_key: str | None = None

    # Cache settings
    cache_enabled: bool = True
    cache_directory: Path | None = None
    cache_ttl_seconds: int = 3600

    # Rate limiting (V2 tiers: Free=5, Light=60, Standard=120, Premium=500)
    requests_per_minute: int = 60

    @classmethod
    def from_environment(cls) -> JQuantsConfig:
        """Load configuration from environment variables."""
        cache_dir = os.environ.get("JQUANTS_CACHE_DIR")
        return cls(
            api_key=os.environ.get("JQUANTS_API_KEY"),
            cache_enabled=os.environ.get("JQUANTS_CACHE_ENABLED", "true").lower() == "true",
            cache_directory=Path(cache_dir) if cache_dir else None,
            cache_ttl_seconds=int(os.environ.get("JQUANTS_CACHE_TTL", "3600")),
            requests_per_minute=int(os.environ.get("JQUANTS_RATE_LIMIT", "60")),
        )

    @classmethod
    def from_toml(cls, path: Path | None = None) -> JQuantsConfig:
        """Load configuration from TOML file."""
        if _tomllib is None:
            raise ImportError(
                "tomllib/tomli is required for TOML config. "
                "Install with: pip install tomli (Python < 3.11)"
            )

        if path is None:
            # Try default locations
            default_paths = [
                Path.home() / ".jquants" / "config.toml",
                Path.home() / ".config" / "jquants" / "config.toml",
                Path(".jquants.toml"),
            ]
            for default_path in default_paths:
                if default_path.exists():
                    path = default_path
                    break

        if path is None or not path.exists():
            return cls()

        with open(path, "rb") as f:
            data = _tomllib.load(f)

        auth = data.get("auth", {})
        cache = data.get("cache", {})
        rate_limit = data.get("rate_limit", {})

        cache_dir = cache.get("directory")
        return cls(
            api_key=auth.get("api_key"),
            cache_enabled=cache.get("enabled", True),
            cache_directory=Path(cache_dir).expanduser() if cache_dir else None,
            cache_ttl_seconds=cache.get("ttl_seconds", 3600),
            requests_per_minute=rate_limit.get("requests_per_minute", 60),
        )

    @classmethod
    def load(cls, config_path: Path | None = None) -> JQuantsConfig:
        """Load configuration with priority: environment > TOML file > defaults."""
        # Start with TOML config or defaults
        config = cls.from_toml(config_path)

        # Override with environment variables
        env_config = cls.from_environment()

        if env_config.api_key:
            config.api_key = env_config.api_key
        if os.environ.get("JQUANTS_CACHE_ENABLED"):
            config.cache_enabled = env_config.cache_enabled
        if os.environ.get("JQUANTS_CACHE_DIR"):
            config.cache_directory = env_config.cache_directory
        if os.environ.get("JQUANTS_CACHE_TTL"):
            config.cache_ttl_seconds = env_config.cache_ttl_seconds
        if os.environ.get("JQUANTS_RATE_LIMIT"):
            config.requests_per_minute = env_config.requests_per_minute

        return config

    def has_api_key(self) -> bool:
        """Check if API key is available."""
        return bool(self.api_key)
