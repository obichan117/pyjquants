"""Options classes for derivatives data (yfinance-style API)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pandas as pd

from pyjquants.adapters.endpoints import INDEX_OPTIONS, OPTIONS
from pyjquants.domain.base import CodeBasedEntity, DomainEntity
from pyjquants.domain.utils import fetch_history
from pyjquants.infra.config import Tier
from pyjquants.infra.decorators import requires_tier

if TYPE_CHECKING:
    from pyjquants.infra.session import Session


class Options(CodeBasedEntity):
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
        super().__init__(code, session)

    @requires_tier(Tier.PREMIUM)
    def history(
        self,
        period: str | None = "30d",
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> pd.DataFrame:
        """Get options price history (yfinance-style).

        Requires Premium tier.

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            start: Start date (YYYY-MM-DD string or date object)
            end: End date (YYYY-MM-DD string or date object)

        Returns:
            DataFrame with columns: date, code, contract_month, strike_price, put_call,
            open, high, low, close, volume, open_interest, implied_volatility, etc.
        """
        return fetch_history(
            client=self._client,
            endpoint=OPTIONS,
            period=period,
            start=start,
            end=end,
            code=self.code,
        )


class IndexOptions(DomainEntity):
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
        super().__init__(session)

    def __repr__(self) -> str:
        return "IndexOptions()"

    def __str__(self) -> str:
        return "Nikkei 225 Index Options"

    @requires_tier(Tier.STANDARD)
    def history(
        self,
        period: str | None = "30d",
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> pd.DataFrame:
        """Get Nikkei 225 index options price history.

        Requires Standard tier or higher.

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            start: Start date (YYYY-MM-DD string or date object)
            end: End date (YYYY-MM-DD string or date object)

        Returns:
            DataFrame with columns: date, code, contract_month, strike_price, put_call,
            open, high, low, close, volume, open_interest, implied_volatility, etc.
        """
        return fetch_history(
            client=self._client,
            endpoint=INDEX_OPTIONS,
            period=period,
            start=start,
            end=end,
        )

    @classmethod
    def nikkei225(cls, session: Session | None = None) -> IndexOptions:
        """Factory method for Nikkei 225 index options.

        Args:
            session: Optional session

        Returns:
            IndexOptions instance for Nikkei 225
        """
        return cls(session=session)
