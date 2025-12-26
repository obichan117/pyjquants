"""
PyJQuants - Investor-friendly OOP Python library for J-Quants API.

Usage:
    import pyjquants as pjq

    # Env vars JQUANTS_MAIL_ADDRESS & JQUANTS_PASSWORD are auto-read
    stock = pjq.Stock("7203")
    stock.name              # "Toyota Motor Corporation"
    stock.prices            # Recent 30 days DataFrame

    # Trading simulation
    trader = pjq.Trader(initial_cash=10_000_000)
    trader.buy(stock, 100)
"""

from pyjquants.core.session import Session, set_global_session
from pyjquants.core.exceptions import (
    PyJQuantsError,
    AuthenticationError,
    TokenExpiredError,
    APIError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ConfigurationError,
)

# Entities
from pyjquants.entities.stock import Stock
from pyjquants.entities.index import Index

# Collections
from pyjquants.collections.market import Market
from pyjquants.collections.universe import Universe

# Trading
from pyjquants.trading.order import Order, Execution
from pyjquants.trading.portfolio import Portfolio, Position
from pyjquants.trading.trader import Trader

# Models
from pyjquants.models.enums import (
    MarketSegment,
    OrderSide,
    OrderStatus,
    OrderType,
    OptionType,
)
from pyjquants.models.company import Sector
from pyjquants.models.price import PriceBar

__version__ = "0.1.0"

__all__ = [
    # Version
    "__version__",
    # Session
    "Session",
    "set_global_session",
    # Exceptions
    "PyJQuantsError",
    "AuthenticationError",
    "TokenExpiredError",
    "APIError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
    "ConfigurationError",
    # Entities
    "Stock",
    "Index",
    # Collections
    "Market",
    "Universe",
    # Trading
    "Order",
    "Execution",
    "Portfolio",
    "Position",
    "Trader",
    # Models/Enums
    "MarketSegment",
    "OrderSide",
    "OrderStatus",
    "OrderType",
    "OptionType",
    "Sector",
    "PriceBar",
]
