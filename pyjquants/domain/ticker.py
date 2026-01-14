"""Ticker class for accessing stock data (yfinance-style API)."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from typing import TYPE_CHECKING

import pandas as pd

from pyjquants.adapters.endpoints import (
    DAILY_QUOTES,
    DAILY_QUOTES_AM,
    DIVIDENDS,
    FINANCIAL_DETAILS,
    LISTED_INFO,
    STATEMENTS,
)
from pyjquants.domain.base import DomainEntity
from pyjquants.domain.info import TickerInfo
from pyjquants.domain.utils import fetch_history
from pyjquants.infra.client import JQuantsClient
from pyjquants.infra.config import Tier
from pyjquants.infra.decorators import requires_tier
from pyjquants.infra.exceptions import TickerNotFoundError
from pyjquants.infra.session import _get_global_session

if TYPE_CHECKING:
    from pyjquants.domain.models import StockInfo
    from pyjquants.infra.session import Session


class Ticker(DomainEntity):
    """Stock ticker for J-Quants API (yfinance-style API).

    Example:
        >>> ticker = Ticker("7203")
        >>> print(ticker.info.name)  # トヨタ自動車
        >>> df = ticker.history(period="30d")
    """

    def __init__(self, code: str, session: Session | None = None) -> None:
        """Initialize ticker with stock code.

        Args:
            code: Stock code (e.g., "7203" for Toyota)
        """
        super().__init__(session)
        self.code = str(code)
        self._info_cache: StockInfo | None = None
        self._ticker_info_cache: TickerInfo | None = None

    def __repr__(self) -> str:
        return f"Ticker('{self.code}')"

    # === INFO ===

    def _load_stock_info(self) -> StockInfo:
        """Load stock info from API."""
        if self._info_cache is None:
            infos = self._client.fetch_list(LISTED_INFO, {"code": self.code})
            if not infos:
                raise TickerNotFoundError(self.code)
            self._info_cache = infos[0]
        return self._info_cache

    @property
    def info(self) -> TickerInfo:
        """Stock information (lazy loaded, cached).

        Returns:
            TickerInfo object with name, sector, market, etc.
        """
        if self._ticker_info_cache is None:
            stock_info = self._load_stock_info()
            self._ticker_info_cache = TickerInfo.from_stock_info(stock_info)
        return self._ticker_info_cache

    # === HISTORY ===

    def history(
        self,
        period: str | None = "30d",
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> pd.DataFrame:
        """Get price history (yfinance-style).

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            start: Start date (YYYY-MM-DD string or date object)
            end: End date (YYYY-MM-DD string or date object)

        Returns:
            DataFrame with columns: date, open, high, low, close, volume, adjusted_close
        """
        return fetch_history(
            client=self._client,
            endpoint=DAILY_QUOTES,
            period=period,
            start=start,
            end=end,
            code=self.code,
        )

    @requires_tier(Tier.PREMIUM)
    def history_am(
        self,
        period: str | None = "30d",
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> pd.DataFrame:
        """Get morning session (AM) price history.

        Returns prices from the morning trading session only (9:00-11:30 JST).
        Useful for intraday analysis or when you need morning-only prices.

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            start: Start date (YYYY-MM-DD string or date object)
            end: End date (YYYY-MM-DD string or date object)

        Returns:
            DataFrame with columns: date, open, high, low, close, volume, adjusted_close
        """
        return fetch_history(
            client=self._client,
            endpoint=DAILY_QUOTES_AM,
            period=period,
            start=start,
            end=end,
            code=self.code,
        )

    # === FINANCIALS ===

    @property
    def financials(self) -> pd.DataFrame:
        """Financial statements."""
        return self._client.fetch_dataframe(STATEMENTS, {"code": self.code})

    @property
    @requires_tier(Tier.PREMIUM)
    def dividends(self) -> pd.DataFrame:
        """Dividend history (Premium tier)."""
        return self._client.fetch_dataframe(DIVIDENDS, {"code": self.code})

    @property
    @requires_tier(Tier.PREMIUM)
    def financial_details(self) -> pd.DataFrame:
        """Full financial statement data (BS/PL/CF) (Premium tier).

        Provides detailed balance sheet, income statement, and cash flow data.
        More comprehensive than the `financials` property.
        """
        return self._client.fetch_dataframe(FINANCIAL_DETAILS, {"code": self.code})


    # === CACHE CONTROL ===

    def refresh(self) -> None:
        """Clear cached data to force fresh fetch on next access."""
        self._info_cache = None
        self._ticker_info_cache = None



# === MODULE-LEVEL FUNCTIONS ===


def _fetch_ticker_history(
    code: str,
    period: str | None,
    start: str | date | None,
    end: str | date | None,
    session: Session | None,
) -> tuple[str, pd.DataFrame]:
    """Fetch history for a single ticker. Returns (code, df) tuple."""
    ticker = Ticker(code, session=session)
    df = ticker.history(period=period, start=start, end=end)
    return code, df


def download(
    codes: list[str],
    period: str | None = "30d",
    start: str | date | None = None,
    end: str | date | None = None,
    session: Session | None = None,
    threads: bool | int = True,
) -> pd.DataFrame:
    """Download price data for multiple tickers (yfinance-style).

    Args:
        codes: List of stock codes
        period: Time period (e.g., "30d", "1y")
        start: Start date
        end: End date
        session: Optional session
        threads: Use threading for faster downloads.
            - True: Use optimal thread count (min of cpu_count or len(codes))
            - False: Sequential download (useful for debugging)
            - int: Use specified number of threads

    Returns:
        Wide-format DataFrame with date index and columns for each ticker's close price

    Example:
        >>> df = pjq.download(["7203", "6758", "9984"], period="30d")
        >>> df = pjq.download(["7203", "6758"], threads=False)  # Sequential
        >>> df = pjq.download(["7203", "6758"], threads=4)  # 4 threads
    """
    if not codes:
        return pd.DataFrame()

    # Determine thread count
    if threads is False:
        max_workers = 1
    elif threads is True:
        max_workers = min(os.cpu_count() or 4, len(codes), 10)
    else:
        max_workers = min(threads, len(codes))

    dfs: dict[str, pd.DataFrame] = {}

    if max_workers == 1:
        # Sequential download
        for code in codes:
            code, df = _fetch_ticker_history(code, period, start, end, session)
            if not df.empty:
                dfs[code] = df
    else:
        # Threaded download
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    _fetch_ticker_history, code, period, start, end, session
                ): code
                for code in codes
            }
            for future in as_completed(futures):
                code, df = future.result()
                if not df.empty:
                    dfs[code] = df

    if not dfs:
        return pd.DataFrame()

    # Combine DataFrames preserving original order
    result_dfs = []
    for code in codes:
        if code in dfs:
            df = dfs[code][["date", "close"]].copy()
            df = df.rename(columns={"close": code})
            result_dfs.append(df.set_index("date"))

    if not result_dfs:
        return pd.DataFrame()

    result = result_dfs[0]
    for df in result_dfs[1:]:
        result = result.join(df, how="outer")

    return result.reset_index()


def search(
    query: str,
    session: Session | None = None,
) -> list[Ticker]:
    """Search for tickers by name or code.

    Args:
        query: Search query (matches company name or code)
        session: Optional session

    Returns:
        List of matching Ticker objects
    """
    session = session or _get_global_session()
    client = JQuantsClient(session)

    infos = client.fetch_list(LISTED_INFO)
    query_lower = query.lower()

    matching = [
        info
        for info in infos
        if query_lower in info.code.lower()
        or query_lower in info.company_name.lower()
        or (info.company_name_english and query_lower in info.company_name_english.lower())
    ]

    return [Ticker(info.code, session) for info in matching]
