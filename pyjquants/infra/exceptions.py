"""Exception hierarchy for pyjquants."""

from __future__ import annotations


class PyJQuantsError(Exception):
    """Base exception for all pyjquants errors."""

    pass


class AuthenticationError(PyJQuantsError):
    """Authentication failed (invalid API key)."""

    pass


class APIError(PyJQuantsError):
    """API request failed."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class RateLimitError(APIError):
    """Rate limit exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(status_code=429, message=message)


class NotFoundError(APIError):
    """Requested resource not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(status_code=404, message=message)


class ValidationError(PyJQuantsError):
    """Invalid input parameters."""

    pass


class ConfigurationError(PyJQuantsError):
    """Configuration error (missing credentials, invalid config file, etc.)."""

    pass


class TierError(PyJQuantsError):
    """Operation requires a higher subscription tier."""

    def __init__(self, method: str, required_tier: str, current_tier: str) -> None:
        self.method = method
        self.required_tier = required_tier
        self.current_tier = current_tier
        super().__init__(
            f"{method}() requires {required_tier}+ tier, but you have {current_tier}"
        )


class TickerNotFoundError(NotFoundError):
    """Ticker not found in J-Quants API."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Ticker not found: {code}")
