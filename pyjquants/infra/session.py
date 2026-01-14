"""HTTP session with API key authentication, caching, and rate limiting."""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Iterator
from typing import Any

import requests

from pyjquants.infra.cache import Cache, NullCache, TTLCache
from pyjquants.infra.config import JQuantsConfig, Tier
from pyjquants.infra.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    RateLimitError,
)

BASE_URL = "https://api.jquants.com/v2"

# Global session instance
_global_session: Session | None = None
_global_session_lock = threading.Lock()


def _get_global_session() -> Session:
    """Get or create the global session instance."""
    global _global_session
    with _global_session_lock:
        if _global_session is None:
            _global_session = Session()
        return _global_session


def set_global_session(session: Session) -> None:
    """Set the global session instance."""
    global _global_session
    with _global_session_lock:
        _global_session = session


class RateLimiter:
    """Thread-safe rate limiter for API calls."""

    def __init__(self, requests_per_minute: int = 60) -> None:
        self._requests_per_minute = requests_per_minute
        self._request_timestamps: deque[float] = deque()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block until rate limit allows request."""
        with self._lock:
            current_time = time.time()

            # Remove timestamps older than 1 minute
            while self._request_timestamps and current_time - self._request_timestamps[0] > 60:
                self._request_timestamps.popleft()

            # Wait if at rate limit
            if len(self._request_timestamps) >= self._requests_per_minute:
                wait_time = 60 - (current_time - self._request_timestamps[0])
                if wait_time > 0:
                    time.sleep(wait_time)
                    current_time = time.time()
                    while (
                        self._request_timestamps and current_time - self._request_timestamps[0] > 60
                    ):
                        self._request_timestamps.popleft()

            self._request_timestamps.append(time.time())


class Session:
    """HTTP session with API key authentication, caching, and rate limiting.

    V2 API uses simple API key authentication via x-api-key header.
    Get your API key from the J-Quants dashboard.

    Example:
        # Via environment variable (recommended)
        os.environ["JQUANTS_API_KEY"] = "your_api_key"
        session = Session()

        # Or explicit
        session = Session(api_key="your_api_key")
    """

    def __init__(
        self,
        api_key: str | None = None,
        config: JQuantsConfig | None = None,
        cache: Cache | None = None,
    ) -> None:
        if config is None:
            config = JQuantsConfig.load()

        # Override config with explicit parameter
        if api_key:
            config.api_key = api_key

        self._config = config
        self._api_key = config.api_key
        self._rate_limiter = RateLimiter(config.requests_per_minute)
        self._http_session = requests.Session()

        # Setup cache
        if cache is not None:
            self._cache = cache
        elif config.cache_enabled:
            self._cache = TTLCache(default_ttl=config.cache_ttl_seconds)
        else:
            self._cache = NullCache()

        # Validate API key is available
        if not self._api_key:
            raise ConfigurationError(
                "No API key available. Set JQUANTS_API_KEY environment variable "
                "or pass api_key parameter."
            )

    @property
    def is_authenticated(self) -> bool:
        """Check if session has API key."""
        return bool(self._api_key)

    @property
    def tier(self) -> Tier:
        """Get subscription tier."""
        return self._config.tier

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None, use_cache: bool = True
    ) -> dict[str, Any]:
        """Make authenticated GET request."""
        return self._request("GET", endpoint, params=params, use_cache=use_cache)

    def get_paginated(
        self, endpoint: str, params: dict[str, Any] | None = None, data_key: str = "data"
    ) -> Iterator[dict[str, Any]]:
        """Iterate through paginated API responses.

        V2 API uses unified 'data' key for all responses.
        """
        params = params.copy() if params else {}

        while True:
            response = self.get(endpoint, params, use_cache=False)
            yield from response.get(data_key, [])

            pagination_key = response.get("pagination_key")
            if not pagination_key:
                break
            params["pagination_key"] = pagination_key

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """Make an authenticated API request."""
        self._rate_limiter.acquire()

        # Check cache for GET requests
        if method == "GET" and use_cache:
            cache_key = self._cache.make_key(endpoint, params)
            cached = self._cache.get(cache_key)
            if cached is not None:
                return dict(cached)

        # V2 uses x-api-key header
        headers = {"x-api-key": self._api_key}

        # Make request
        url = f"{BASE_URL}{endpoint}"
        response = self._http_session.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
        )

        # Handle errors
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        if response.status_code == 403:
            raise AuthenticationError("API key does not have access to this endpoint")

        if response.status_code >= 400:
            raise APIError(response.status_code, response.text)

        data: dict[str, Any] = response.json()

        # Cache successful GET responses
        if method == "GET" and use_cache:
            cache_key = self._cache.make_key(endpoint, params)
            self._cache.set(cache_key, data)

        return data

    def close(self) -> None:
        """Close the HTTP session."""
        self._http_session.close()

    def __enter__(self) -> Session:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
