"""Index class for market index data (yfinance-style API)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pandas as pd

from pyjquants.adapters.endpoints import INDEX_PRICES, TOPIX
from pyjquants.domain.base import CodeBasedEntity
from pyjquants.domain.utils import fetch_history
from pyjquants.infra.config import Tier
from pyjquants.infra.exceptions import TierError
from pyjquants.infra.session import _get_global_session

if TYPE_CHECKING:
    from pyjquants.infra.session import Session


# Known index codes
TOPIX_CODE = "0000"
NIKKEI225_CODE = "0001"


class Index(CodeBasedEntity):
    """Market index with yfinance-style API.

    Example:
        >>> topix = Index.topix()
        >>> df = topix.history(period="30d")
        >>> df = topix.history(start="2024-01-01", end="2024-12-31")
    """

    _KNOWN_INDICES = {
        TOPIX_CODE: "TOPIX",
        NIKKEI225_CODE: "Nikkei 225",
    }

    def __init__(self, code: str, name: str | None = None, session: Session | None = None) -> None:
        """Initialize Index.

        Args:
            code: Index code (e.g., "0000" for TOPIX)
            name: Index name (optional, auto-detected for known indices)
            session: Optional session (uses global session if not provided)
        """
        super().__init__(code, session)
        self._name = name or self._KNOWN_INDICES.get(code)

    @property
    def name(self) -> str:
        """Index name."""
        return self._name or self.code

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    # === HISTORY (yfinance-style) ===

    def history(
        self,
        period: str | None = "30d",
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> pd.DataFrame:
        """Get price history (yfinance-style).

        Note: Non-TOPIX indices (e.g., Nikkei 225) require Standard tier or higher.

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            start: Start date (YYYY-MM-DD string or date object)
            end: End date (YYYY-MM-DD string or date object)

        Returns:
            DataFrame with columns: date, open, high, low, close
        """
        # Use TOPIX-specific endpoint for TOPIX, otherwise general index endpoint
        if self.code == TOPIX_CODE:
            # TOPIX endpoint doesn't need code param
            return fetch_history(
                client=self._client,
                endpoint=TOPIX,
                period=period,
                start=start,
                end=end,
            )
        else:
            # Non-TOPIX indices require Standard+ tier
            if self._session.tier < Tier.STANDARD:
                raise TierError(
                    method="history",
                    required_tier=Tier.STANDARD.value,
                    current_tier=self._session.tier.value,
                )
            return fetch_history(
                client=self._client,
                endpoint=INDEX_PRICES,
                period=period,
                start=start,
                end=end,
                code=self.code,
            )

    # === FACTORY METHODS ===

    @classmethod
    def topix(cls, session: Session | None = None) -> Index:
        """Get TOPIX index."""
        return cls(code=TOPIX_CODE, name="TOPIX", session=session)

    @classmethod
    def nikkei225(cls, session: Session | None = None) -> Index:
        """Get Nikkei 225 index."""
        return cls(code=NIKKEI225_CODE, name="Nikkei 225", session=session)

    @classmethod
    def all(cls, session: Session | None = None) -> list[Index]:
        """Get all known indices."""
        session = session or _get_global_session()
        return [
            cls(code=code, name=name, session=session)
            for code, name in cls._KNOWN_INDICES.items()
        ]

