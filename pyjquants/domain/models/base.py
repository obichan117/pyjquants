"""Base model and enums for pyjquants."""

from __future__ import annotations

import datetime
from decimal import Decimal
from enum import Enum
from typing import Annotated, Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic import BeforeValidator, ConfigDict

# === Validator functions ===


def _parse_date(v: Any) -> datetime.date:
    """Parse date from various formats (YYYYMMDD or YYYY-MM-DD)."""
    if isinstance(v, datetime.date):
        return v
    if isinstance(v, str):
        if "-" in v:
            return datetime.date.fromisoformat(v)
        return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
    raise ValueError(f"Cannot parse date: {v}")


def _parse_date_optional(v: Any) -> datetime.date | None:
    """Parse optional date."""
    if v is None or v == "":
        return None
    return _parse_date(v)


def _parse_decimal(v: Any) -> Decimal | None:
    """Parse decimal from various formats."""
    if v is None or v == "":
        return None
    return Decimal(str(v))


def _parse_decimal_required(v: Any) -> Decimal:
    """Parse required decimal."""
    if v is None or v == "":
        raise ValueError("Decimal value is required")
    return Decimal(str(v))


# === Annotated types for reuse ===

JQuantsDate = Annotated[datetime.date, BeforeValidator(_parse_date)]
JQuantsDateOptional = Annotated[datetime.date | None, BeforeValidator(_parse_date_optional)]
JQuantsDecimal = Annotated[Decimal | None, BeforeValidator(_parse_decimal)]
JQuantsDecimalRequired = Annotated[Decimal, BeforeValidator(_parse_decimal_required)]


class BaseModel(PydanticBaseModel):
    """Base model with common configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class MarketSegment(str, Enum):
    """Market segment classification."""

    TSE_PRIME = "Prime"
    TSE_STANDARD = "Standard"
    TSE_GROWTH = "Growth"
    TOKYO_PRO = "Tokyo Pro Market"
    OTHER = "Other"

    @classmethod
    def from_code(cls, code: str) -> MarketSegment:
        """Convert market code to MarketSegment."""
        code_map = {
            "0111": cls.TSE_PRIME,
            "0112": cls.TSE_STANDARD,
            "0113": cls.TSE_GROWTH,
            "0105": cls.TOKYO_PRO,
            "0109": cls.OTHER,
        }
        return code_map.get(code, cls.OTHER)
