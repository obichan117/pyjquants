"""Company-related models."""

from __future__ import annotations

import datetime
from typing import Any

from pydantic import Field, field_validator

from pyjquants.domain.models.base import BaseModel, MarketSegment


class Sector(BaseModel):
    """Sector classification."""

    code: str
    name: str
    name_english: str | None = None

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Sector({self.code}: {self.name})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Sector):
            return self.code == other.code
        if isinstance(other, str):
            return self.code == other or self.name == other
        return False

    def __hash__(self) -> int:
        return hash(self.code)


class StockInfo(BaseModel):
    """Listed company basic information."""

    code: str = Field(alias="Code")
    company_name: str = Field(alias="CompanyName")
    company_name_english: str | None = Field(alias="CompanyNameEnglish", default=None)

    sector_17_code: str = Field(alias="Sector17Code")
    sector_17_name: str = Field(alias="Sector17CodeName")
    sector_33_code: str = Field(alias="Sector33Code")
    sector_33_name: str = Field(alias="Sector33CodeName")

    market_code: str = Field(alias="MarketCode")
    market_name: str = Field(alias="MarketCodeName")

    scale_category: str | None = Field(alias="ScaleCategory", default=None)
    listing_date: datetime.date | None = Field(alias="Date", default=None)

    @field_validator("listing_date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date | None:
        if v is None or v == "":
            return None
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        return None

    @property
    def sector_17(self) -> Sector:
        return Sector(code=self.sector_17_code, name=self.sector_17_name)

    @property
    def sector_33(self) -> Sector:
        return Sector(code=self.sector_33_code, name=self.sector_33_name)

    @property
    def market_segment(self) -> MarketSegment:
        return MarketSegment.from_code(self.market_code)
