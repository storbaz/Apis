"""
Bootstrap coffee production data from a CSV file.

Expected CSV format (FAOSTAT style):
Area Code,Area,Item Code,Item,Element,Year,Unit,Value

Usage:
  1. Download FAOSTAT bulk data from https://www.fao.org/faostat/en/
  2. Extract the CSV for "Production > Crops and livestock products"
  3. Run: python -m scripts.bootstrap_data --csv path/to/faostat_production.csv

For initial testing, you can also use the Kaggle ICO Coffee Dataset:
  https://www.kaggle.com/datasets/yamaerenay/ico-coffee-dataset-worldwide
"""
import argparse
import asyncio
import csv
from pathlib import Path
from typing import Optional

from datetime import date
from sqlalchemy import select
from app.core.database import async_session, engine, Base
from app.models.coffee import Country, Production, Price


def parse_number(value: str) -> Optional[float]:
    if not value or value.strip() in ("", "NA", "N/A", "-"):
        return None
    try:
        return float(value.replace(",", "").strip())
    except (ValueError, TypeError):
        return None


async def load_faostat_csv(csv_path: str):
    path = Path(csv_path)
    if not path.exists():
        print(f"File not found: {csv_path}")
        return

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            loaded = 0
            skipped = 0

            for row in reader:
                area_code = row.get("Area Code", "").strip()
                area_name = row.get("Area", "").strip()
                item = row.get("Item", "").strip()
                element = row.get("Element", "").strip()
                year_str = row.get("Year", "").strip()
                value_str = row.get("Value", "").strip()

                if not year_str or not value_str:
                    skipped += 1
                    continue

                year = int(year_str)
                value = parse_number(value_str)

                if value is None:
                    skipped += 1
                    continue

                country_result = await session.execute(
                    select(Country).where(Country.code == area_code)
                )
                country = country_result.scalar_one_or_none()

                if not country:
                    country = Country(code=area_code, name=area_name)
                    session.add(country)
                    await session.flush()

                bags_60kg = None
                tonnes = None

                if "Production" in element:
                    if "tonnes" in row.get("Unit", "").lower() or "ton" in row.get("Unit", "").lower():
                        tonnes = value
                        bags_60kg = value / 60
                    else:
                        bags_60kg = value
                        tonnes = value * 60
                else:
                    continue

                existing = await session.execute(
                    select(Production).where(
                        Production.country_id == country.id,
                        Production.year == year,
                        Production.variety == "all",
                    )
                )
                if existing.scalar_one_or_none():
                    skipped += 1
                    continue

                production = Production(
                    country_id=country.id,
                    year=year,
                    variety="all",
                    bags_60kg=round(bags_60kg, 2),
                    tonnes=round(tonnes, 2),
                    source="fao",
                )
                session.add(production)
                loaded += 1

                if loaded % 100 == 0:
                    await session.commit()
                    print(f"  Loaded {loaded} records...")

            await session.commit()
            print(f"Done: {loaded} loaded, {skipped} skipped")


async def load_sample_data():
    """Load sample data for testing without a CSV file."""
    SAMPLE_DATA = [
        {"code": "BR", "name": "Brazil", "productions": [
            {"year": 2020, "bags": 63400000, "tonnes": 3804000000},
            {"year": 2021, "bags": 56100000, "tonnes": 3366000000},
            {"year": 2022, "bags": 66400000, "tonnes": 3984000000},
            {"year": 2023, "bags": 69900000, "tonnes": 4194000000},
            {"year": 2024, "bags": 64700000, "tonnes": 3882000000},
        ]},
        {"code": "VN", "name": "Vietnam", "productions": [
            {"year": 2020, "bags": 29000000, "tonnes": 1740000000},
            {"year": 2021, "bags": 31400000, "tonnes": 1884000000},
            {"year": 2022, "bags": 29000000, "tonnes": 1740000000},
            {"year": 2023, "bags": 30100000, "tonnes": 1806000000},
            {"year": 2024, "bags": 29500000, "tonnes": 1770000000},
        ]},
        {"code": "CO", "name": "Colombia", "productions": [
            {"year": 2020, "bags": 14300000, "tonnes": 858000000},
            {"year": 2021, "bags": 12760000, "tonnes": 765600000},
            {"year": 2022, "bags": 11500000, "tonnes": 690000000},
            {"year": 2023, "bags": 12400000, "tonnes": 744000000},
            {"year": 2024, "bags": 13800000, "tonnes": 828000000},
        ]},
        {"code": "ID", "name": "Indonesia", "productions": [
            {"year": 2020, "bags": 12000000, "tonnes": 720000000},
            {"year": 2021, "bags": 11200000, "tonnes": 672000000},
            {"year": 2022, "bags": 10800000, "tonnes": 648000000},
            {"year": 2023, "bags": 11400000, "tonnes": 684000000},
            {"year": 2024, "bags": 12600000, "tonnes": 756000000},
        ]},
        {"code": "ET", "name": "Ethiopia", "productions": [
            {"year": 2020, "bags": 7300000, "tonnes": 438000000},
            {"year": 2021, "bags": 7500000, "tonnes": 450000000},
            {"year": 2022, "bags": 8600000, "tonnes": 516000000},
            {"year": 2023, "bags": 8360000, "tonnes": 501600000},
            {"year": 2024, "bags": 11560000, "tonnes": 693600000},
        ]},
        {"code": "HN", "name": "Honduras", "productions": [
            {"year": 2020, "bags": 6100000, "tonnes": 366000000},
            {"year": 2021, "bags": 5700000, "tonnes": 342000000},
            {"year": 2022, "bags": 5050000, "tonnes": 303000000},
            {"year": 2023, "bags": 5300000, "tonnes": 318000000},
            {"year": 2024, "bags": 5800000, "tonnes": 348000000},
        ]},
        {"code": "UG", "name": "Uganda", "productions": [
            {"year": 2020, "bags": 5800000, "tonnes": 348000000},
            {"year": 2021, "bags": 6200000, "tonnes": 372000000},
            {"year": 2022, "bags": 5800000, "tonnes": 348000000},
            {"year": 2023, "bags": 6400000, "tonnes": 384000000},
            {"year": 2024, "bags": 6880000, "tonnes": 412800000},
        ]},
        {"code": "PE", "name": "Peru", "productions": [
            {"year": 2020, "bags": 3800000, "tonnes": 228000000},
            {"year": 2021, "bags": 3475000, "tonnes": 208500000},
            {"year": 2022, "bags": 3912000, "tonnes": 234720000},
            {"year": 2023, "bags": 4200000, "tonnes": 252000000},
            {"year": 2024, "bags": 4200000, "tonnes": 252000000},
        ]},
        {"code": "IN", "name": "India", "productions": [
            {"year": 2020, "bags": 5800000, "tonnes": 348000000},
            {"year": 2021, "bags": 5200000, "tonnes": 312000000},
            {"year": 2022, "bags": 5600000, "tonnes": 336000000},
            {"year": 2023, "bags": 5400000, "tonnes": 324000000},
            {"year": 2024, "bags": 6050000, "tonnes": 363000000},
        ]},
        {"code": "GT", "name": "Guatemala", "productions": [
            {"year": 2020, "bags": 3600000, "tonnes": 216000000},
            {"year": 2021, "bags": 3150000, "tonnes": 189000000},
            {"year": 2022, "bags": 3339000, "tonnes": 200340000},
            {"year": 2023, "bags": 3000000, "tonnes": 180000000},
            {"year": 2024, "bags": 3410000, "tonnes": 204600000},
        ]},
    ]

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        for country_data in SAMPLE_DATA:
            existing = await session.execute(
                select(Country).where(Country.code == country_data["code"])
            )
            country = existing.scalar_one_or_none()

            if not country:
                country = Country(code=country_data["code"], name=country_data["name"])
                session.add(country)
                await session.flush()

            for prod in country_data["productions"]:
                existing_prod = await session.execute(
                    select(Production).where(
                        Production.country_id == country.id,
                        Production.year == prod["year"],
                        Production.variety == "all",
                    )
                )
                if existing_prod.scalar_one_or_none():
                    continue

                session.add(Production(
                    country_id=country.id,
                    year=prod["year"],
                    variety="all",
                    bags_60kg=prod["bags"],
                    tonnes=prod["tonnes"],
                    source="usda",
                ))

        await session.commit()
        print("Sample production data loaded!")


async def load_sample_prices():
    """Load sample price data for testing."""
    SAMPLE_PRICES = [
        {"date": date(2024, 1, 15), "variety": "arabica", "price": 185.20},
        {"date": date(2024, 2, 15), "variety": "arabica", "price": 178.45},
        {"date": date(2024, 3, 15), "variety": "arabica", "price": 192.30},
        {"date": date(2024, 4, 15), "variety": "arabica", "price": 198.75},
        {"date": date(2024, 5, 15), "variety": "arabica", "price": 210.50},
        {"date": date(2024, 6, 15), "variety": "arabica", "price": 225.80},
        {"date": date(2024, 7, 15), "variety": "arabica", "price": 240.15},
        {"date": date(2024, 8, 15), "variety": "arabica", "price": 255.90},
        {"date": date(2024, 9, 15), "variety": "arabica", "price": 248.60},
        {"date": date(2024, 10, 15), "variety": "arabica", "price": 262.40},
        {"date": date(2024, 11, 15), "variety": "arabica", "price": 275.30},
        {"date": date(2024, 12, 15), "variety": "arabica", "price": 288.95},
        {"date": date(2025, 1, 15), "variety": "arabica", "price": 310.20},
        {"date": date(2025, 2, 15), "variety": "arabica", "price": 325.50},
        {"date": date(2025, 3, 15), "variety": "arabica", "price": 340.80},
        {"date": date(2025, 4, 15), "variety": "arabica", "price": 355.10},
        {"date": date(2025, 5, 15), "variety": "arabica", "price": 370.25},
        {"date": date(2025, 6, 15), "variety": "arabica", "price": 385.40},
        {"date": date(2024, 1, 15), "variety": "robusta", "price": 2850.00},
        {"date": date(2024, 2, 15), "variety": "robusta", "price": 2780.00},
        {"date": date(2024, 3, 15), "variety": "robusta", "price": 2920.00},
        {"date": date(2024, 4, 15), "variety": "robusta", "price": 2980.00},
        {"date": date(2024, 5, 15), "variety": "robusta", "price": 3100.00},
        {"date": date(2024, 6, 15), "variety": "robusta", "price": 3250.00},
        {"date": date(2024, 7, 15), "variety": "robusta", "price": 3400.00},
        {"date": date(2024, 8, 15), "variety": "robusta", "price": 3550.00},
        {"date": date(2024, 9, 15), "variety": "robusta", "price": 3480.00},
        {"date": date(2024, 10, 15), "variety": "robusta", "price": 3620.00},
        {"date": date(2024, 11, 15), "variety": "robusta", "price": 3750.00},
        {"date": date(2024, 12, 15), "variety": "robusta", "price": 3890.00},
        {"date": date(2025, 1, 15), "variety": "robusta", "price": 4100.00},
        {"date": date(2025, 2, 15), "variety": "robusta", "price": 4250.00},
        {"date": date(2025, 3, 15), "variety": "robusta", "price": 4400.00},
        {"date": date(2025, 4, 15), "variety": "robusta", "price": 4550.00},
        {"date": date(2025, 5, 15), "variety": "robusta", "price": 4700.00},
        {"date": date(2025, 6, 15), "variety": "robusta", "price": 4850.00},
    ]

    async with async_session() as session:
        count = 0
        for p in SAMPLE_PRICES:
            existing = await session.execute(
                select(Price).where(Price.date == p["date"], Price.variety == p["variety"])
            )
            if not existing.scalar_one_or_none():
                session.add(Price(
                    date=p["date"],
                    variety=p["variety"],
                    price_usd_cents_per_lb=p["price"],
                    source="sample",
                ))
                count += 1

        await session.commit()
        print(f"Loaded {count} sample price records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap coffee data")
    parser.add_argument("--csv", type=str, help="Path to FAOSTAT CSV file")
    parser.add_argument("--sample", action="store_true", help="Load sample data")
    parser.add_argument("--prices", action="store_true", help="Load sample prices")
    args = parser.parse_args()

    if args.csv:
        asyncio.run(load_faostat_csv(args.csv))
    elif args.sample:
        asyncio.run(load_sample_data())
    elif args.prices:
        asyncio.run(load_sample_prices())
    else:
        print("Usage:")
        print("  python -m scripts.bootstrap_data --sample")
        print("  python -m scripts.bootstrap_data --prices")
        print("  python -m scripts.bootstrap_data --csv path/to/faostat.csv")
