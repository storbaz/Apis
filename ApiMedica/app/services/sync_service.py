"""
Orchestration service for syncing all data sources.
Run: python -m app.services.sync_service
"""
import asyncio
import logging
from datetime import datetime

from sqlalchemy import select

from app.core.database import async_session, engine, Base
from app.models.coffee import Country, Price
from app.services import fao_service, usda_service, fred_service

logger = logging.getLogger(__name__)


async def sync_prices_from_fred():
    """Sync coffee prices from FRED/IMF."""
    logger.info("Syncing prices from FRED...")

    arabica_data = await fred_service.get_coffee_prices("PCOFFOTMUSDM")
    robusta_data = await fred_service.get_coffee_prices("PCOFFROBUSDM")

    async with async_session() as session:
        count = 0
        for obs in arabica_data:
            if obs.get("value") == ".":
                continue
            try:
                date_str = obs["date"]
                price = float(obs["value"])
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

                existing = await session.execute(
                    select(Price).where(Price.date == date_obj, Price.variety == "arabica")
                )
                if not existing.scalar_one_or_none():
                    session.add(Price(
                        date=date_obj,
                        variety="arabica",
                        price_usd_cents_per_lb=price,
                        source="imf",
                    ))
                    count += 1
            except Exception as e:
                logger.warning(f"Failed to parse arabica price: {e}")

        for obs in robusta_data:
            if obs.get("value") == ".":
                continue
            try:
                date_str = obs["date"]
                price = float(obs["value"])
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

                existing = await session.execute(
                    select(Price).where(Price.date == date_obj, Price.variety == "robusta")
                )
                if not existing.scalar_one_or_none():
                    session.add(Price(
                        date=date_obj,
                        variety="robusta",
                        price_usd_cents_per_lb=price,
                        source="imf",
                    ))
                    count += 1
            except Exception as e:
                logger.warning(f"Failed to parse robusta price: {e}")

        await session.commit()
        logger.info(f"Synced {count} price records from FRED")


async def sync_all():
    """Run all sync tasks."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting full data sync...")

    await sync_prices_from_fred()

    logger.info("Data sync complete!")


if __name__ == "__main__":
    asyncio.run(sync_all())
