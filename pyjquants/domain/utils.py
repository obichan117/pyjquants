"""Shared utility functions for domain layer."""

from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from pyjquants.adapters.endpoints import Endpoint
    from pyjquants.infra.client import JQuantsClient


def fetch_history(
    client: JQuantsClient,
    endpoint: Endpoint[Any],
    period: str | None = "30d",
    start: str | date | None = None,
    end: str | date | None = None,
    code: str | None = None,
    extra_params: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Fetch historical data with yfinance-style period/date handling.

    Args:
        client: JQuantsClient instance
        endpoint: API endpoint definition
        period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
        start: Start date (YYYY-MM-DD string or date object)
        end: End date (YYYY-MM-DD string or date object)
        code: Optional code (stock, index, futures, etc.)
        extra_params: Additional query parameters

    Returns:
        DataFrame with historical data, sorted by date
    """
    # Parse dates
    start_date = parse_date(start) if start is not None else None
    end_date = parse_date(end) if end is not None else None

    # If no explicit dates, use period
    if start_date is None and end_date is None:
        days = parse_period(period or "30d")
        end_date = date.today()
        start_date = end_date - timedelta(days=days + 15)  # Buffer for non-trading days

    # Build params
    params = client.date_params(code=code, start=start_date, end=end_date)
    if extra_params:
        params.update(extra_params)

    # Fetch data
    df = client.fetch_dataframe(endpoint, params)

    if df.empty:
        return df

    # Trim to requested period if using period parameter
    if period and start is None and end is None:
        days = parse_period(period)
        df = df.tail(days)

    return df.reset_index(drop=True)


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
