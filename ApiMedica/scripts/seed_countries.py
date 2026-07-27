"""
Seed the countries table with major coffee producing countries.
Run: python -m scripts.seed_countries
"""
import asyncio
from sqlalchemy import select
from app.core.database import async_session, engine, Base
from app.models.coffee import Country

COFFEE_COUNTRIES = [
    {"code": "BR", "name": "Brazil", "region": "Americas", "sub_region": "South America"},
    {"code": "VN", "name": "Vietnam", "region": "Asia", "sub_region": "Southeast Asia"},
    {"code": "ID", "name": "Indonesia", "region": "Asia", "sub_region": "Southeast Asia"},
    {"code": "CO", "name": "Colombia", "region": "Americas", "sub_region": "South America"},
    {"code": "ET", "name": "Ethiopia", "region": "Africa", "sub_region": "Eastern Africa"},
    {"code": "HN", "name": "Honduras", "region": "Americas", "sub_region": "Central America"},
    {"code": "UG", "name": "Uganda", "region": "Africa", "sub_region": "Eastern Africa"},
    {"code": "PE", "name": "Peru", "region": "Americas", "sub_region": "South America"},
    {"code": "IN", "name": "India", "region": "Asia", "sub_region": "Southern Asia"},
    {"code": "CF", "name": "Central African Republic", "region": "Africa", "sub_region": "Central Africa"},
    {"code": "GT", "name": "Guatemala", "region": "Americas", "sub_region": "Central America"},
    {"code": "GN", "name": "Guinea", "region": "Africa", "sub_region": "Western Africa"},
    {"code": "MX", "name": "Mexico", "region": "Americas", "sub_region": "Central America"},
    {"code": "LA", "name": "Laos", "region": "Asia", "sub_region": "Southeast Asia"},
    {"code": "NI", "name": "Nicaragua", "region": "Americas", "sub_region": "Central America"},
    {"code": "CN", "name": "China", "region": "Asia", "sub_region": "Eastern Asia"},
    {"code": "CI", "name": "Ivory Coast", "region": "Africa", "sub_region": "Western Africa"},
    {"code": "CR", "name": "Costa Rica", "region": "Americas", "sub_region": "Central America"},
    {"code": "TZ", "name": "Tanzania", "region": "Africa", "sub_region": "Eastern Africa"},
    {"code": "CD", "name": "Democratic Republic of the Congo", "region": "Africa", "sub_region": "Central Africa"},
    {"code": "VE", "name": "Venezuela", "region": "Americas", "sub_region": "South America"},
    {"code": "MG", "name": "Madagascar", "region": "Africa", "sub_region": "Eastern Africa"},
    {"code": "KE", "name": "Kenya", "region": "Africa", "sub_region": "Eastern Africa"},
    {"code": "PG", "name": "Papua New Guinea", "region": "Oceania", "sub_region": "Melanesia"},
    {"code": "SV", "name": "El Salvador", "region": "Americas", "sub_region": "Central America"},
    {"code": "YE", "name": "Yemen", "region": "Asia", "sub_region": "Western Asia"},
    {"code": "TH", "name": "Thailand", "region": "Asia", "sub_region": "Southeast Asia"},
    {"code": "EC", "name": "Ecuador", "region": "Americas", "sub_region": "South America"},
    {"code": "CAM", "name": "Cameroon", "region": "Africa", "sub_region": "Central Africa"},
    {"code": "TG", "name": "Togo", "region": "Africa", "sub_region": "Western Africa"},
    {"code": "RW", "name": "Rwanda", "region": "Africa", "sub_region": "Eastern Africa"},
    {"code": "PH", "name": "Philippines", "region": "Asia", "sub_region": "Southeast Asia"},
    {"code": "MM", "name": "Myanmar", "region": "Asia", "sub_region": "Southeast Asia"},
    {"code": "US", "name": "United States", "region": "Americas", "sub_region": "Northern America"},
    {"code": "DE", "name": "Germany", "region": "Europe", "sub_region": "Western Europe"},
    {"code": "JP", "name": "Japan", "region": "Asia", "sub_region": "Eastern Asia"},
    {"code": "IT", "name": "Italy", "region": "Europe", "sub_region": "Southern Europe"},
    {"code": "FR", "name": "France", "region": "Europe", "sub_region": "Western Europe"},
    {"code": "GB", "name": "United Kingdom", "region": "Europe", "sub_region": "Northern Europe"},
    {"code": "NL", "name": "Netherlands", "region": "Europe", "sub_region": "Western Europe"},
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        for country_data in COFFEE_COUNTRIES:
            existing = await session.execute(
                select(Country).where(Country.code == country_data["code"])
            )
            if not existing.scalar_one_or_none():
                session.add(Country(**country_data))
        await session.commit()
        print(f"Seeded {len(COFFEE_COUNTRIES)} countries")


if __name__ == "__main__":
    asyncio.run(seed())
