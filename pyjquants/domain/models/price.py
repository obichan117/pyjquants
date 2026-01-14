"""Price-related models for J-Quants API V2."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field, field_validator

from pyjquants.domain.models.base import BaseModel


class PriceBar(BaseModel):
    """Single OHLCV price bar.

    V2 API uses abbreviated field names (O, H, L, C, Vo, Va).
    """

    date: datetime.date = Field(alias="Date")
    open: Decimal = Field(alias="O")
    high: Decimal = Field(alias="H")
    low: Decimal = Field(alias="L")
    close: Decimal = Field(alias="C")
    volume: int = Field(alias="Vo", default=0)
    turnover_value: Decimal | None = Field(alias="Va", default=None)

    adjustment_factor: Decimal = Field(alias="AdjFactor", default=Decimal("1.0"))
    adjustment_open: Decimal | None = Field(alias="AdjO", default=None)
    adjustment_high: Decimal | None = Field(alias="AdjH", default=None)
    adjustment_low: Decimal | None = Field(alias="AdjL", default=None)
    adjustment_close: Decimal | None = Field(alias="AdjC", default=None)
    adjustment_volume: int | None = Field(alias="AdjVo", default=None)

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

    @field_validator("open", "high", "low", "close", "turnover_value", mode="before")
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None:
            return None
        return Decimal(str(v))

    @field_validator(
        "adjustment_factor",
        "adjustment_open",
        "adjustment_high",
        "adjustment_low",
        "adjustment_close",
        mode="before",
    )
    @classmethod
    def parse_adjustment_decimal(cls, v: Any) -> Decimal | None:
        if v is None:
            return None
        return Decimal(str(v))

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


class IndexPrice(BaseModel):
    """Index price data.

    V2 API uses abbreviated field names.
    """

    date: datetime.date = Field(alias="Date")
    code: str = Field(alias="Code")
    open: Decimal | None = Field(alias="O", default=None)
    high: Decimal | None = Field(alias="H", default=None)
    low: Decimal | None = Field(alias="L", default=None)
    close: Decimal | None = Field(alias="C", default=None)

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

    @field_validator("open", "high", "low", "close", mode="before")
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date,
            "open": float(self.open) if self.open else None,
            "high": float(self.high) if self.high else None,
            "low": float(self.low) if self.low else None,
            "close": float(self.close) if self.close else None,
        }
