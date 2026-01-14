"""Derivatives-related models for futures and options."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjquants.domain.models.base import (
    BaseModel,
    JQuantsDate,
    JQuantsDateOptional,
    JQuantsDecimal,
)


class FuturesPrice(BaseModel):
    """Futures OHLC price data.

    Contains whole day, morning session, night session, and day session prices.
    """

    date: JQuantsDate = Field(alias="Date")
    code: str = Field(alias="Code")
    product_category: str = Field(alias="ProdCat")
    contract_month: str = Field(alias="CM")

    # Whole day OHLC
    open: JQuantsDecimal = Field(alias="O", default=None)
    high: JQuantsDecimal = Field(alias="H", default=None)
    low: JQuantsDecimal = Field(alias="L", default=None)
    close: JQuantsDecimal = Field(alias="C", default=None)

    # Volume & Interest
    volume: int | None = Field(alias="Vo", default=None)
    open_interest: int | None = Field(alias="OI", default=None)
    turnover_value: JQuantsDecimal = Field(alias="Va", default=None)

    # Settlement
    settlement_price: JQuantsDecimal = Field(alias="Settle", default=None)
    last_trading_day: JQuantsDateOptional = Field(alias="LTD", default=None)
    special_quotation_day: JQuantsDateOptional = Field(alias="SQD", default=None)

    # Morning session (optional)
    morning_open: JQuantsDecimal = Field(alias="MO", default=None)
    morning_high: JQuantsDecimal = Field(alias="MH", default=None)
    morning_low: JQuantsDecimal = Field(alias="ML", default=None)
    morning_close: JQuantsDecimal = Field(alias="MC", default=None)

    # Night session (optional)
    night_open: JQuantsDecimal = Field(alias="EO", default=None)
    night_high: JQuantsDecimal = Field(alias="EH", default=None)
    night_low: JQuantsDecimal = Field(alias="EL", default=None)
    night_close: JQuantsDecimal = Field(alias="EC", default=None)

    # Day session (optional)
    day_open: JQuantsDecimal = Field(alias="AO", default=None)
    day_high: JQuantsDecimal = Field(alias="AH", default=None)
    day_low: JQuantsDecimal = Field(alias="AL", default=None)
    day_close: JQuantsDecimal = Field(alias="AC", default=None)

    # Additional fields
    central_contract_month_flag: str | None = Field(alias="CCMFlag", default=None)

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

    date: JQuantsDate = Field(alias="Date")
    code: str = Field(alias="Code")
    product_category: str = Field(alias="ProdCat")
    contract_month: str = Field(alias="CM")

    # Option-specific
    strike_price: JQuantsDecimal = Field(alias="Strike", default=None)
    put_call_division: str | None = Field(alias="PCDiv", default=None)  # 1=Put, 2=Call
    underlying_code: str | None = Field(alias="UndSSO", default=None)

    # Whole day OHLC
    open: JQuantsDecimal = Field(alias="O", default=None)
    high: JQuantsDecimal = Field(alias="H", default=None)
    low: JQuantsDecimal = Field(alias="L", default=None)
    close: JQuantsDecimal = Field(alias="C", default=None)

    # Volume & Interest
    volume: int | None = Field(alias="Vo", default=None)
    open_interest: int | None = Field(alias="OI", default=None)
    turnover_value: JQuantsDecimal = Field(alias="Va", default=None)

    # Greeks/Pricing
    settlement_price: JQuantsDecimal = Field(alias="Settle", default=None)
    theoretical_price: JQuantsDecimal = Field(alias="Theo", default=None)
    implied_volatility: JQuantsDecimal = Field(alias="IV", default=None)
    base_volatility: JQuantsDecimal = Field(alias="BaseVol", default=None)
    underlying_price: JQuantsDecimal = Field(alias="UnderPx", default=None)
    interest_rate: JQuantsDecimal = Field(alias="IR", default=None)

    # Morning session (optional)
    morning_open: JQuantsDecimal = Field(alias="MO", default=None)
    morning_high: JQuantsDecimal = Field(alias="MH", default=None)
    morning_low: JQuantsDecimal = Field(alias="ML", default=None)
    morning_close: JQuantsDecimal = Field(alias="MC", default=None)

    # Night session (optional)
    night_open: JQuantsDecimal = Field(alias="EO", default=None)
    night_high: JQuantsDecimal = Field(alias="EH", default=None)
    night_low: JQuantsDecimal = Field(alias="EL", default=None)
    night_close: JQuantsDecimal = Field(alias="EC", default=None)

    # Day session (optional)
    day_open: JQuantsDecimal = Field(alias="AO", default=None)
    day_high: JQuantsDecimal = Field(alias="AH", default=None)
    day_low: JQuantsDecimal = Field(alias="AL", default=None)
    day_close: JQuantsDecimal = Field(alias="AC", default=None)

    # Dates
    last_trading_day: JQuantsDateOptional = Field(alias="LTD", default=None)
    special_quotation_day: JQuantsDateOptional = Field(alias="SQD", default=None)

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
