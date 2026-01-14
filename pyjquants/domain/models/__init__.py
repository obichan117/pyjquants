"""Domain models for pyjquants.

Re-exports all models for backward compatibility.
"""

from pyjquants.domain.models.base import BaseModel, MarketSegment
from pyjquants.domain.models.company import Sector, StockInfo
from pyjquants.domain.models.derivatives import FuturesPrice, OptionsPrice
from pyjquants.domain.models.financial import (
    Dividend,
    EarningsAnnouncement,
    FinancialDetails,
    FinancialStatement,
)
from pyjquants.domain.models.market import (
    BreakdownTrade,
    InvestorTrades,
    MarginAlert,
    MarginInterest,
    ShortSaleReport,
    ShortSelling,
    TradingCalendarDay,
)
from pyjquants.domain.models.price import AMPriceBar, IndexPrice, PriceBar

__all__ = [
    # Base
    "BaseModel",
    "MarketSegment",
    # Price
    "PriceBar",
    "AMPriceBar",
    "IndexPrice",
    # Company
    "Sector",
    "StockInfo",
    # Financial
    "FinancialStatement",
    "FinancialDetails",
    "Dividend",
    "EarningsAnnouncement",
    # Market
    "TradingCalendarDay",
    "MarginInterest",
    "ShortSelling",
    "InvestorTrades",
    "BreakdownTrade",
    "ShortSaleReport",
    "MarginAlert",
    # Derivatives
    "FuturesPrice",
    "OptionsPrice",
]
