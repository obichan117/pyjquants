"""TickerInfo class for stock profile information."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyjquants.domain.models import StockInfo


@dataclass
class TickerInfo:
    """Stock profile information (like pykabutan's Profile).

    Provides easy access to company information.

    Example:
        >>> ticker = Ticker("7203")
        >>> ticker.info.name  # "トヨタ自動車"
        >>> ticker.info.sector  # "輸送用機器"
        >>> ticker.info.market  # "Prime"
    """

    code: str
    name: str
    name_english: str | None
    sector: str
    sector_code: str
    sector_17: str
    sector_17_code: str
    market: str
    market_code: str
    listing_date: date | None

    @classmethod
    def from_stock_info(cls, info: StockInfo) -> TickerInfo:
        """Create TickerInfo from StockInfo model."""
        return cls(
            code=info.code,
            name=info.company_name,
            name_english=info.company_name_english,
            sector=info.sector_33_name,
            sector_code=info.sector_33_code,
            sector_17=info.sector_17_name,
            sector_17_code=info.sector_17_code,
            market=info.market_segment.value,
            market_code=info.market_code,
            listing_date=info.listing_date,
        )

    def __repr__(self) -> str:
        return f"TickerInfo({self.code}: {self.name})"
