"""
Service for syncing price data from FRED (Federal Reserve Bank of St. Louis).
Documentation: https://fred.stlouisfed.org/docs/api/fred/
Data: IMF Primary Commodity Prices
"""
import httpx
import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


async def get_coffee_prices(
    series_id: str = "PCOFFOTMUSDM",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> list:
    """
    Fetch coffee price data from FRED.
    
    Series IDs:
    - PCOFFOTMUSDM: Coffee, Other Mild Arabicas (monthly)
    - PCOFFROBUSDM: Coffee, Robusta (monthly)
    
    Returns monthly prices in US cents per pound.
    """
    params = {
        "series_id": series_id,
        "api_key": settings.FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1000,
    }
    if start_date:
        params["observation_start"] = start_date
    if end_date:
        params["observation_end"] = end_date

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(FRED_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("observations", [])
        except Exception as e:
            logger.error(f"FRED request failed: {e}")
            return []


async def get_latest_price(series_id: str = "PCOFFOTMUSDM") -> Optional[dict]:
    """Get the most recent coffee price."""
    params = {
        "series_id": series_id,
        "api_key": settings.FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(FRED_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            observations = data.get("observations", [])
            return observations[0] if observations else None
        except Exception as e:
            logger.error(f"FRED latest price request failed: {e}")
            return None
