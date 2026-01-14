"""Options classes for derivatives data (yfinance-style API)."""

from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

import pandas as pd

from pyjquants.adapters.endpoints import INDEX_OPTIONS, OPTIONS
from pyjquants.domain.utils import parse_date, parse_period
from pyjquants.infra.client import JQuantsClient
from pyjquants.infra.session import _get_global_session

if TYPE_CHECKING:
    from pyjquants.infra.session import Session


class Options:
    """Options contract with yfinance-style API.

    Example:
        >>> options = Options("NK225C25000")
        >>> df = options.history(period="30d")
        >>> df = options.history(start="2024-01-01", end="2024-12-31")
    """

    def __init__(self, code: str, session: Session | None = None) -> None:
        """Initialize Options.

        Args:
            code: Options contract code
            session: Optional session (uses global session if not provided)
        """
        self.code = code
        self._session = session or _get_global_session()
        self._client = JQuantsClient(self._session)

    def __repr__(self) -> str:
        return f"Options('{self.code}')"

    def __str__(self) -> str:
        return f"Options({self.code})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Options):
            return self.code == other.code
        if isinstance(other, str):
            return self.code == other
        return False

    def __hash__(self) -> int:
        return hash(self.code)

    def history(
        self,
        period: str | None = "30d",
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> pd.DataFrame:
        """Get options price history (yfinance-style).

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            start: Start date (YYYY-MM-DD string or date object)
            end: End date (YYYY-MM-DD string or date object)

        Returns:
            DataFrame with columns: date, code, contract_month, strike_price, put_call,
            open, high, low, close, volume, open_interest, implied_volatility, etc.
        """
        # Parse dates
        start_date = parse_date(start) if start is not None else None
        end_date = parse_date(end) if end is not None else None

        # If no explicit dates, use period
        if start_date is None and end_date is None:
            days = parse_period(period or "30d")
            end_date = date.today()
            start_date = end_date - timedelta(days=days + 15)  # Buffer for non-trading days

        params = self._client.date_params(code=self.code, start=start_date, end=end_date)

        df = self._client.fetch_dataframe(OPTIONS, params)

        if df.empty:
            return df

        # Trim to requested period if using period parameter
        if period and start is None and end is None:
            days = parse_period(period)
            df = df.tail(days)

        return df.reset_index(drop=True)


class IndexOptions:
    """Nikkei 225 index options with yfinance-style API.

    Example:
        >>> idx_opts = IndexOptions.nikkei225()
        >>> df = idx_opts.history(period="30d")
        >>> df = idx_opts.history(start="2024-01-01", end="2024-12-31")
    """

    def __init__(self, session: Session | None = None) -> None:
        """Initialize IndexOptions.

        Args:
            session: Optional session (uses global session if not provided)
        """
        self._session = session or _get_global_session()
        self._client = JQuantsClient(self._session)

    def __repr__(self) -> str:
        return "IndexOptions()"

    def __str__(self) -> str:
        return "Nikkei 225 Index Options"

    def history(
        self,
        period: str | None = "30d",
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> pd.DataFrame:
        """Get Nikkei 225 index options price history.

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            start: Start date (YYYY-MM-DD string or date object)
            end: End date (YYYY-MM-DD string or date object)

        Returns:
            DataFrame with columns: date, code, contract_month, strike_price, put_call,
            open, high, low, close, volume, open_interest, implied_volatility, etc.
        """
        # Parse dates
        start_date = parse_date(start) if start is not None else None
        end_date = parse_date(end) if end is not None else None

        # If no explicit dates, use period
        if start_date is None and end_date is None:
            days = parse_period(period or "30d")
            end_date = date.today()
            start_date = end_date - timedelta(days=days + 15)  # Buffer for non-trading days

        params = self._client.date_params(start=start_date, end=end_date)

        df = self._client.fetch_dataframe(INDEX_OPTIONS, params)

        if df.empty:
            return df

        # Trim to requested period if using period parameter
        if period and start is None and end is None:
            days = parse_period(period)
            df = df.tail(days)

        return df.reset_index(drop=True)

    @classmethod
    def nikkei225(cls, session: Session | None = None) -> IndexOptions:
        """Factory method for Nikkei 225 index options.

        Args:
            session: Optional session

        Returns:
            IndexOptions instance for Nikkei 225
        """
        return cls(session=session)
