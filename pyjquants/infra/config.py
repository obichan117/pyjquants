"""Configuration loading from environment variables and TOML files."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import ModuleType


class Tier(Enum):
    """J-Quants subscription tiers.

    Each tier has different rate limits and endpoint access:
    - FREE: 5 req/min, basic endpoints only
    - LIGHT: 60 req/min, basic endpoints only
    - STANDARD: 120 req/min, most endpoints
    - PREMIUM: 500 req/min, all endpoints + intraday data
    """

    FREE = "free"
    LIGHT = "light"
    STANDARD = "standard"
    PREMIUM = "premium"

    def __ge__(self, other: Tier) -> bool:
        order = [Tier.FREE, Tier.LIGHT, Tier.STANDARD, Tier.PREMIUM]
        return order.index(self) >= order.index(other)

    def __gt__(self, other: Tier) -> bool:
        order = [Tier.FREE, Tier.LIGHT, Tier.STANDARD, Tier.PREMIUM]
        return order.index(self) > order.index(other)

    def __le__(self, other: Tier) -> bool:
        order = [Tier.FREE, Tier.LIGHT, Tier.STANDARD, Tier.PREMIUM]
        return order.index(self) <= order.index(other)

    def __lt__(self, other: Tier) -> bool:
        order = [Tier.FREE, Tier.LIGHT, Tier.STANDARD, Tier.PREMIUM]
        return order.index(self) < order.index(other)


TIER_RATE_LIMITS: dict[Tier, int] = {
    Tier.FREE: 5,
    Tier.LIGHT: 60,
    Tier.STANDARD: 120,
    Tier.PREMIUM: 500,
}

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

    # Subscription tier (determines rate limit and endpoint access)
    tier: Tier = Tier.LIGHT

    # Cache settings
    cache_enabled: bool = True
    cache_directory: Path | None = None
    cache_ttl_seconds: int = 3600

    @property
    def requests_per_minute(self) -> int:
        """Get rate limit based on tier."""
        return TIER_RATE_LIMITS[self.tier]

    @classmethod
    def _parse_tier(cls, tier_str: str | None, rate_limit: str | None) -> Tier:
        """Parse tier from environment, with backwards compat for rate limit."""
        # Explicit tier takes precedence
        if tier_str:
            return Tier(tier_str.lower())

        # Backwards compat: infer tier from rate limit
        if rate_limit:
            limit = int(rate_limit)
            if limit >= 500:
                return Tier.PREMIUM
            if limit >= 120:
                return Tier.STANDARD
            if limit >= 60:
                return Tier.LIGHT
            return Tier.FREE

        return Tier.LIGHT  # Default

    @classmethod
    def from_environment(cls) -> JQuantsConfig:
        """Load configuration from environment variables."""
        cache_dir = os.environ.get("JQUANTS_CACHE_DIR")
        tier = cls._parse_tier(
            os.environ.get("JQUANTS_TIER"),
            os.environ.get("JQUANTS_RATE_LIMIT"),
        )
        return cls(
            api_key=os.environ.get("JQUANTS_API_KEY"),
            tier=tier,
            cache_enabled=os.environ.get("JQUANTS_CACHE_ENABLED", "true").lower() == "true",
            cache_directory=Path(cache_dir) if cache_dir else None,
            cache_ttl_seconds=int(os.environ.get("JQUANTS_CACHE_TTL", "3600")),
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

        # Parse tier (with backwards compat for rate_limit)
        tier_str = auth.get("tier")
        rate_limit_val = data.get("rate_limit", {}).get("requests_per_minute")
        tier = cls._parse_tier(tier_str, str(rate_limit_val) if rate_limit_val else None)

        cache_dir = cache.get("directory")
        return cls(
            api_key=auth.get("api_key"),
            tier=tier,
            cache_enabled=cache.get("enabled", True),
            cache_directory=Path(cache_dir).expanduser() if cache_dir else None,
            cache_ttl_seconds=cache.get("ttl_seconds", 3600),
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
        if os.environ.get("JQUANTS_TIER") or os.environ.get("JQUANTS_RATE_LIMIT"):
            config.tier = env_config.tier
        if os.environ.get("JQUANTS_CACHE_ENABLED"):
            config.cache_enabled = env_config.cache_enabled
        if os.environ.get("JQUANTS_CACHE_DIR"):
            config.cache_directory = env_config.cache_directory
        if os.environ.get("JQUANTS_CACHE_TTL"):
            config.cache_ttl_seconds = env_config.cache_ttl_seconds

        return config

    def has_api_key(self) -> bool:
        """Check if API key is available."""
        return bool(self.api_key)
