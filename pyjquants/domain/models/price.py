"""Price-related models for J-Quants API V2."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import Field

from pyjquants.domain.models.base import (
    BaseModel,
    JQuantsDate,
    JQuantsDecimal,
    JQuantsDecimalRequired,
)


class PriceBar(BaseModel):
    """Single OHLCV price bar.

    V2 API uses abbreviated field names (O, H, L, C, Vo, Va).
    """

    date: JQuantsDate = Field(alias="Date")
    open: JQuantsDecimalRequired = Field(alias="O")
    high: JQuantsDecimalRequired = Field(alias="H")
    low: JQuantsDecimalRequired = Field(alias="L")
    close: JQuantsDecimalRequired = Field(alias="C")
    volume: int = Field(alias="Vo", default=0)
    turnover_value: JQuantsDecimal = Field(alias="Va", default=None)

    adjustment_factor: JQuantsDecimalRequired = Field(alias="AdjFactor", default=Decimal("1.0"))
    adjustment_open: JQuantsDecimal = Field(alias="AdjO", default=None)
    adjustment_high: JQuantsDecimal = Field(alias="AdjH", default=None)
    adjustment_low: JQuantsDecimal = Field(alias="AdjL", default=None)
    adjustment_close: JQuantsDecimal = Field(alias="AdjC", default=None)
    adjustment_volume: int | None = Field(alias="AdjVo", default=None)

    # Limit flags
    upper_limit: str | None = Field(alias="UL", default=None)
    lower_limit: str | None = Field(alias="LL", default=None)

    # Morning session (Premium only)
    morning_open: JQuantsDecimal = Field(alias="MO", default=None)
    morning_high: JQuantsDecimal = Field(alias="MH", default=None)
    morning_low: JQuantsDecimal = Field(alias="ML", default=None)
    morning_close: JQuantsDecimal = Field(alias="MC", default=None)
    morning_upper_limit: str | None = Field(alias="MUL", default=None)
    morning_lower_limit: str | None = Field(alias="MLL", default=None)
    morning_volume: int | None = Field(alias="MVo", default=None)
    morning_turnover_value: JQuantsDecimal = Field(alias="MVa", default=None)
    morning_adj_open: JQuantsDecimal = Field(alias="MAdjO", default=None)
    morning_adj_high: JQuantsDecimal = Field(alias="MAdjH", default=None)
    morning_adj_low: JQuantsDecimal = Field(alias="MAdjL", default=None)
    morning_adj_close: JQuantsDecimal = Field(alias="MAdjC", default=None)
    morning_adj_volume: int | None = Field(alias="MAdjVo", default=None)

    # Afternoon session (Premium only)
    afternoon_open: JQuantsDecimal = Field(alias="AO", default=None)
    afternoon_high: JQuantsDecimal = Field(alias="AH", default=None)
    afternoon_low: JQuantsDecimal = Field(alias="AL", default=None)
    afternoon_close: JQuantsDecimal = Field(alias="AC", default=None)
    afternoon_upper_limit: str | None = Field(alias="AUL", default=None)
    afternoon_lower_limit: str | None = Field(alias="ALL", default=None)
    afternoon_volume: int | None = Field(alias="AVo", default=None)
    afternoon_turnover_value: JQuantsDecimal = Field(alias="AVa", default=None)
    afternoon_adj_open: JQuantsDecimal = Field(alias="AAdjO", default=None)
    afternoon_adj_high: JQuantsDecimal = Field(alias="AAdjH", default=None)
    afternoon_adj_low: JQuantsDecimal = Field(alias="AAdjL", default=None)
    afternoon_adj_close: JQuantsDecimal = Field(alias="AAdjC", default=None)
    afternoon_adj_volume: int | None = Field(alias="AAdjVo", default=None)

    @property
    def adjusted_open(self) -> Decimal:
        if self.adjustment_open is not None:
            return self.adjustment_open
        return self.open * self.adjustment_factor

    @property
    def adjusted_high(self) -> Decimal:
        if self.adjustment_high is not None:
            return self.adjustment_high
        return self.high * self.adjustment_factor

    @property
    def adjusted_low(self) -> Decimal:
        if self.adjustment_low is not None:
            return self.adjustment_low
        return self.low * self.adjustment_factor

    @property
    def adjusted_close(self) -> Decimal:
        if self.adjustment_close is not None:
            return self.adjustment_close
        return self.close * self.adjustment_factor

    @property
    def adjusted_volume(self) -> int:
        if self.adjustment_volume is not None:
            return self.adjustment_volume
        if self.adjustment_factor == Decimal("1.0"):
            return self.volume
        return int(self.volume / self.adjustment_factor)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for DataFrame creation."""
        return {
            "date": self.date,
            "open": float(self.open),
            "high": float(self.high),
            "low": float(self.low),
            "close": float(self.close),
            "volume": self.volume,
            "adjusted_close": float(self.adjusted_close),
        }


class AMPriceBar(BaseModel):
    """Morning session (AM) price bar.

    V2 API uses MO, MH, ML, MC for morning session OHLC.
    Different field names from regular PriceBar (O, H, L, C).
    """

    date: JQuantsDate = Field(alias="Date")
    code: str = Field(alias="Code")
    open: JQuantsDecimal = Field(alias="MO", default=None)
    high: JQuantsDecimal = Field(alias="MH", default=None)
    low: JQuantsDecimal = Field(alias="ML", default=None)
    close: JQuantsDecimal = Field(alias="MC", default=None)
    volume: int | None = Field(alias="MVo", default=None)
    turnover_value: JQuantsDecimal = Field(alias="MVa", default=None)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for DataFrame creation."""
        return {
            "date": self.date,
            "open": float(self.open) if self.open else None,
            "high": float(self.high) if self.high else None,
            "low": float(self.low) if self.low else None,
            "close": float(self.close) if self.close else None,
            "volume": self.volume,
        }


class IndexPrice(BaseModel):
    """Index price data.

    V2 API uses abbreviated field names.
    Note: Code field is optional (not present in TOPIX-specific endpoint).
    """

    date: JQuantsDate = Field(alias="Date")
    code: str | None = Field(alias="Code", default=None)
    open: JQuantsDecimal = Field(alias="O", default=None)
    high: JQuantsDecimal = Field(alias="H", default=None)
    low: JQuantsDecimal = Field(alias="L", default=None)
    close: JQuantsDecimal = Field(alias="C", default=None)

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date,
            "open": float(self.open) if self.open else None,
            "high": float(self.high) if self.high else None,
            "low": float(self.low) if self.low else None,
            "close": float(self.close) if self.close else None,
        }
