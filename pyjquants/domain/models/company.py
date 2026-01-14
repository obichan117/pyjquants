"""Company-related models."""

from __future__ import annotations

from pydantic import Field

from pyjquants.domain.models.base import BaseModel, JQuantsDateOptional, MarketSegment


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
    """Listed company basic information (V2 API abbreviated field names)."""

    code: str = Field(alias="Code")
    company_name: str = Field(alias="CoName")
    company_name_english: str | None = Field(alias="CoNameEn", default=None)

    sector_17_code: str = Field(alias="S17")
    sector_17_name: str = Field(alias="S17Nm")
    sector_33_code: str = Field(alias="S33")
    sector_33_name: str = Field(alias="S33Nm")

    market_code: str = Field(alias="Mkt")
    market_name: str = Field(alias="MktNm")

    scale_category: str | None = Field(alias="ScaleCat", default=None)
    listing_date: JQuantsDateOptional = Field(alias="Date", default=None)

    # V2 new fields
    margin_code: str | None = Field(alias="Mrgn", default=None)
    margin_name: str | None = Field(alias="MrgnNm", default=None)

    @property
    def sector_17(self) -> Sector:
        return Sector(code=self.sector_17_code, name=self.sector_17_name)

    @property
    def sector_33(self) -> Sector:
        return Sector(code=self.sector_33_code, name=self.sector_33_name)

    @property
    def market_segment(self) -> MarketSegment:
        return MarketSegment.from_code(self.market_code)
