"""Derivatives-related models for futures and options."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field, field_validator

from pyjquants.domain.models.base import BaseModel


class FuturesPrice(BaseModel):
    """Futures OHLC price data.

    Contains whole day, morning session, night session, and day session prices.
    """

    date: datetime.date = Field(alias="Date")
    code: str = Field(alias="Code")
    product_category: str = Field(alias="ProdCat")
    contract_month: str = Field(alias="CM")

    # Whole day OHLC
    open: Decimal | None = Field(alias="O", default=None)
    high: Decimal | None = Field(alias="H", default=None)
    low: Decimal | None = Field(alias="L", default=None)
    close: Decimal | None = Field(alias="C", default=None)

    # Volume & Interest
    volume: int | None = Field(alias="Vo", default=None)
    open_interest: int | None = Field(alias="OI", default=None)
    turnover_value: Decimal | None = Field(alias="Va", default=None)

    # Settlement
    settlement_price: Decimal | None = Field(alias="Settle", default=None)
    last_trading_day: datetime.date | None = Field(alias="LTD", default=None)
    special_quotation_day: datetime.date | None = Field(alias="SQD", default=None)

    # Morning session (optional)
    morning_open: Decimal | None = Field(alias="MO", default=None)
    morning_high: Decimal | None = Field(alias="MH", default=None)
    morning_low: Decimal | None = Field(alias="ML", default=None)
    morning_close: Decimal | None = Field(alias="MC", default=None)

    # Night session (optional)
    night_open: Decimal | None = Field(alias="EO", default=None)
    night_high: Decimal | None = Field(alias="EH", default=None)
    night_low: Decimal | None = Field(alias="EL", default=None)
    night_close: Decimal | None = Field(alias="EC", default=None)

    # Day session (optional)
    day_open: Decimal | None = Field(alias="AO", default=None)
    day_high: Decimal | None = Field(alias="AH", default=None)
    day_low: Decimal | None = Field(alias="AL", default=None)
    day_close: Decimal | None = Field(alias="AC", default=None)

    # Additional fields
    central_contract_month_flag: str | None = Field(alias="CCMFlag", default=None)

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date:
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        raise ValueError(f"Cannot parse date: {v}")

    @field_validator("last_trading_day", "special_quotation_day", mode="before")
    @classmethod
    def parse_optional_date(cls, v: Any) -> datetime.date | None:
        if v is None or v == "":
            return None
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        return None

    @field_validator(
        "open", "high", "low", "close",
        "morning_open", "morning_high", "morning_low", "morning_close",
        "night_open", "night_high", "night_low", "night_close",
        "day_open", "day_high", "day_low", "day_close",
        "turnover_value", "settlement_price",
        mode="before",
    )
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for DataFrame creation."""
        return {
            "date": self.date,
            "code": self.code,
            "product_category": self.product_category,
            "contract_month": self.contract_month,
            "open": float(self.open) if self.open else None,
            "high": float(self.high) if self.high else None,
            "low": float(self.low) if self.low else None,
            "close": float(self.close) if self.close else None,
            "volume": self.volume,
            "open_interest": self.open_interest,
            "settlement_price": float(self.settlement_price) if self.settlement_price else None,
        }


class OptionsPrice(BaseModel):
    """Options OHLC price data.

    Contains option-specific fields like strike price, put/call division,
    implied volatility, and theoretical price.
    """

    date: datetime.date = Field(alias="Date")
    code: str = Field(alias="Code")
    product_category: str = Field(alias="ProdCat")
    contract_month: str = Field(alias="CM")

    # Option-specific
    strike_price: Decimal | None = Field(alias="Strike", default=None)
    put_call_division: str | None = Field(alias="PCDiv", default=None)  # 1=Put, 2=Call
    underlying_code: str | None = Field(alias="UndSSO", default=None)

    # Whole day OHLC
    open: Decimal | None = Field(alias="O", default=None)
    high: Decimal | None = Field(alias="H", default=None)
    low: Decimal | None = Field(alias="L", default=None)
    close: Decimal | None = Field(alias="C", default=None)

    # Volume & Interest
    volume: int | None = Field(alias="Vo", default=None)
    open_interest: int | None = Field(alias="OI", default=None)
    turnover_value: Decimal | None = Field(alias="Va", default=None)

    # Greeks/Pricing
    settlement_price: Decimal | None = Field(alias="Settle", default=None)
    theoretical_price: Decimal | None = Field(alias="Theo", default=None)
    implied_volatility: Decimal | None = Field(alias="IV", default=None)
    base_volatility: Decimal | None = Field(alias="BaseVol", default=None)
    underlying_price: Decimal | None = Field(alias="UnderPx", default=None)
    interest_rate: Decimal | None = Field(alias="IR", default=None)

    # Morning session (optional)
    morning_open: Decimal | None = Field(alias="MO", default=None)
    morning_high: Decimal | None = Field(alias="MH", default=None)
    morning_low: Decimal | None = Field(alias="ML", default=None)
    morning_close: Decimal | None = Field(alias="MC", default=None)

    # Night session (optional)
    night_open: Decimal | None = Field(alias="EO", default=None)
    night_high: Decimal | None = Field(alias="EH", default=None)
    night_low: Decimal | None = Field(alias="EL", default=None)
    night_close: Decimal | None = Field(alias="EC", default=None)

    # Day session (optional)
    day_open: Decimal | None = Field(alias="AO", default=None)
    day_high: Decimal | None = Field(alias="AH", default=None)
    day_low: Decimal | None = Field(alias="AL", default=None)
    day_close: Decimal | None = Field(alias="AC", default=None)

    # Dates
    last_trading_day: datetime.date | None = Field(alias="LTD", default=None)
    special_quotation_day: datetime.date | None = Field(alias="SQD", default=None)

    # Additional
    central_contract_month_flag: str | None = Field(alias="CCMFlag", default=None)

    @property
    def is_put(self) -> bool:
        """Check if this is a put option."""
        return self.put_call_division == "1"

    @property
    def is_call(self) -> bool:
        """Check if this is a call option."""
        return self.put_call_division == "2"

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date:
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        raise ValueError(f"Cannot parse date: {v}")

    @field_validator("last_trading_day", "special_quotation_day", mode="before")
    @classmethod
    def parse_optional_date(cls, v: Any) -> datetime.date | None:
        if v is None or v == "":
            return None
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        return None

    @field_validator(
        "open", "high", "low", "close",
        "strike_price", "settlement_price", "theoretical_price",
        "implied_volatility", "base_volatility", "underlying_price", "interest_rate",
        "morning_open", "morning_high", "morning_low", "morning_close",
        "night_open", "night_high", "night_low", "night_close",
        "day_open", "day_high", "day_low", "day_close",
        "turnover_value",
        mode="before",
    )
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for DataFrame creation."""
        return {
            "date": self.date,
            "code": self.code,
            "product_category": self.product_category,
            "contract_month": self.contract_month,
            "strike_price": float(self.strike_price) if self.strike_price else None,
            "put_call": "Put" if self.is_put else ("Call" if self.is_call else None),
            "open": float(self.open) if self.open else None,
            "high": float(self.high) if self.high else None,
            "low": float(self.low) if self.low else None,
            "close": float(self.close) if self.close else None,
            "volume": self.volume,
            "open_interest": self.open_interest,
            "settlement_price": float(self.settlement_price) if self.settlement_price else None,
            "implied_volatility": float(self.implied_volatility) if self.implied_volatility else None,
        }
