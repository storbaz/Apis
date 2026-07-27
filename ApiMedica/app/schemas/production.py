from pydantic import BaseModel
from typing import Optional


class CountryResponse(BaseModel):
    code: str
    name: str
    region: Optional[str] = None
    sub_region: Optional[str] = None

    class Config:
        from_attributes = True


class ProductionResponse(BaseModel):
    country: str
    country_code: str
    year: int
    variety: str
    bags_60kg: Optional[float] = None
    tonnes: Optional[float] = None
    source: str

    class Config:
        from_attributes = True


class PriceResponse(BaseModel):
    date: str
    variety: str
    price_usd_cents_per_lb: float
    source: str

    class Config:
        from_attributes = True


class OverviewResponse(BaseModel):
    total_countries: int
    latest_year: int
    total_production_bags: float
    top_producer: str
    top_producer_bags: float
