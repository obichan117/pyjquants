"""Futures class for derivatives data (yfinance-style API)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pandas as pd

from pyjquants.adapters.endpoints import FUTURES
from pyjquants.domain.utils import fetch_history
from pyjquants.infra.client import JQuantsClient
from pyjquants.infra.config import Tier
from pyjquants.infra.decorators import requires_tier
from pyjquants.infra.session import _get_global_session

if TYPE_CHECKING:
    from pyjquants.infra.session import Session


class Futures:
    """Futures contract with yfinance-style API.

    Example:
        >>> futures = Futures("NK225M")  # Nikkei 225 mini
        >>> df = futures.history(period="30d")
        >>> df = futures.history(start="2024-01-01", end="2024-12-31")
    """

    def __init__(self, code: str, session: Session | None = None) -> None:
        """Initialize Futures.

        Args:
            code: Futures contract code (e.g., product category code)
            session: Optional session (uses global session if not provided)
        """
        self.code = code
        self._session = session or _get_global_session()
        self._client = JQuantsClient(self._session)

    def __repr__(self) -> str:
        return f"Futures('{self.code}')"

    def __str__(self) -> str:
        return f"Futures({self.code})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Futures):
            return self.code == other.code
        if isinstance(other, str):
            return self.code == other
        return False

    def __hash__(self) -> int:
        return hash(self.code)

    @requires_tier(Tier.PREMIUM)
    def history(
        self,
        period: str | None = "30d",
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> pd.DataFrame:
        """Get futures price history (yfinance-style).

        Requires Premium tier.

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            start: Start date (YYYY-MM-DD string or date object)
            end: End date (YYYY-MM-DD string or date object)

        Returns:
            DataFrame with columns: date, code, contract_month, open, high, low, close,
            volume, open_interest, settlement_price, etc.
        """
        return fetch_history(
            client=self._client,
            endpoint=FUTURES,
            period=period,
            start=start,
            end=end,
            code=self.code,
        )
