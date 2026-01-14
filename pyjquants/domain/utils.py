"""Shared utility functions for domain layer."""

from __future__ import annotations

from datetime import date


def parse_period(period: str) -> int:
    """Parse period string to number of days.

    Args:
        period: Period string (e.g., "30d", "1w", "6mo", "1y")

    Returns:
        Number of days

    Examples:
        >>> parse_period("30d")
        30
        >>> parse_period("1w")
        7
        >>> parse_period("6mo")
        180
        >>> parse_period("1y")
        365
    """
    period = period.lower()
    if period.endswith("d"):
        return int(period[:-1])
    elif period.endswith("w"):
        return int(period[:-1]) * 7
    elif period.endswith("mo"):
        return int(period[:-2]) * 30
    elif period.endswith("m") and not period.endswith("mo"):
        return int(period[:-1]) * 30
    elif period.endswith("y"):
        return int(period[:-1]) * 365
    else:
        return int(period)


def parse_date(d: str | date) -> date:
    """Parse date string or return date object.

    Args:
        d: Date string (ISO format) or date object

    Returns:
        date object

    Examples:
        >>> parse_date("2024-01-15")
        date(2024, 1, 15)
        >>> parse_date(date(2024, 1, 15))
        date(2024, 1, 15)
    """
    if isinstance(d, date):
        return d
    return date.fromisoformat(d)
