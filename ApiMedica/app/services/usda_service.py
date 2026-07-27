"""
Service for syncing data from USDA Foreign Agricultural Service API.
Documentation: https://apps.fas.usda.gov/opendatawebV2/
"""
import httpx
import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

USDA_BASE_URL = "https://apps.fas.usda.gov/OpenData/api"


async def _get_headers() -> dict:
    return {"API_KEY": settings.USDA_FAS_API_KEY}


async def get_commodities() -> list:
    """Get list of all PSD commodities."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{USDA_BASE_URL}/psd/commodities",
                headers=await _get_headers(),
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"USDA commodities request failed: {e}")
            return []


async def get_psd_data(commodity_code: str, country_code: str = "all", year: str = "all") -> list:
    """
    Get Production, Supply and Distribution data.
    Coffee commodity codes: 0611100 (Coffee, Green)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{USDA_BASE_URL}/psd/commodity/{commodity_code}/country/{country_code}/year/{year}",
                headers=await _get_headers(),
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"USDA PSD request failed: {e}")
            return []


async def get_export_sales(commodity_code: str, market_year: str) -> list:
    """
    Get export sales data.
    Coffee ESR code: 907030 (Coffee)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{USDA_BASE_URL}/esr/exports/commodityCode/{commodity_code}/allCountries/marketYear/{market_year}",
                headers=await _get_headers(),
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"USDA ESR request failed: {e}")
            return []
