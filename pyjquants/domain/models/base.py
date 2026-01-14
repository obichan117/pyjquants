"""Base model and enums for pyjquants."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


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
