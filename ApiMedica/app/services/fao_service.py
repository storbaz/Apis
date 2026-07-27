"""
Service for syncing data from FAOSTAT API.
Documentation: https://www.fao.org/faostat/en/
API: https://fenixservices.fao.org/faostat/api/v1/en/
"""
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

FAOSTAT_BASE_URL = "https://fenixservices.fao.org/faostat/api/v1/en"


async def get_production_data(
    area_code: Optional[str] = None,
    year: Optional[int] = None,
) -> dict:
    """
    Fetch coffee production data from FAOSTAT.
    Domain: qcl (Crops and livestock products)
    Item: 0661 (Coffee, green)
    Element: 5510 (Production)
    """
    params = {
        "area": area_code or "*",
        "item": "0661",
        "element": "5510",
        "year": str(year) if year else "*",
        "output_type": "json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{FAOSTAT_BASE_URL}/data/QCL",
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"FAOSTAT API error: {e.response.status_code}")
            return {"data": []}
        except Exception as e:
            logger.error(f"FAOSTAT request failed: {e}")
            return {"data": []}


async def get_trade_data(
    area_code: Optional[str] = None,
    year: Optional[int] = None,
) -> dict:
    """
    Fetch coffee trade data from FAOSTAT.
    Domain: TDF (Total Trade)
    Item: 0661 (Coffee, green)
    """
    params = {
        "area": area_code or "*",
        "item": "0661",
        "year": str(year) if year else "*",
        "output_type": "json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{FAOSTAT_BASE_URL}/data/TDF",
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"FAOSTAT trade API error: {e.response.status_code}")
            return {"data": []}
        except Exception as e:
            logger.error(f"FAOSTAT trade request failed: {e}")
            return {"data": []}
