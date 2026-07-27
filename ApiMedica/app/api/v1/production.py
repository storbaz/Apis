from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.deps import get_api_key_owner
from app.models.coffee import Country, Production
from app.models.user import User
from app.schemas.production import ProductionResponse, OverviewResponse, CountryResponse

router = APIRouter(dependencies=[Depends(get_api_key_owner)])


@router.get("/countries")
async def get_countries(
    region: str = Query(None, description="Filter by region"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_api_key_owner),
):
    query = select(Country)
    if region:
        query = query.where(Country.region.ilike(f"%{region}%"))

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Country.name).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)

    data = [CountryResponse.model_validate(c) for c in result.scalars().all()]

    return {
        "data": data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/production")
async def get_production(
    country: str = Query(None, description="Country code or name"),
    year_from: int = Query(None, ge=1961),
    year_to: int = Query(None, le=2030),
    variety: str = Query(None, description="arabica, robusta, all"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_api_key_owner),
):
    query = (
        select(Production, Country)
        .join(Country, Production.country_id == Country.id)
    )

    if country:
        query = query.where(
            (Country.code.ilike(f"%{country}%")) | (Country.name.ilike(f"%{country}%"))
        )
    if year_from:
        query = query.where(Production.year >= year_from)
    if year_to:
        query = query.where(Production.year <= year_to)
    if variety:
        query = query.where(Production.variety == variety)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Production.year.desc(), Country.name)
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)

    data = [
        ProductionResponse(
            country=c.name,
            country_code=c.code,
            year=p.year,
            variety=p.variety,
            bags_60kg=float(p.bags_60kg) if p.bags_60kg else None,
            tonnes=float(p.tonnes) if p.tonnes else None,
            source=p.source,
        )
        for p, c in result.all()
    ]

    return {
        "data": data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/overview")
async def get_overview(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_api_key_owner),
):
    country_count = (await db.execute(select(func.count(Country.id)))).scalar() or 0

    latest_year_result = await db.execute(select(func.max(Production.year)))
    latest_year = latest_year_result.scalar() or 2024

    total_bags_result = await db.execute(
        select(func.sum(Production.bags_60kg)).where(Production.year == latest_year)
    )
    total_bags = float(total_bags_result.scalar() or 0)

    top_query = (
        select(Country.name, func.sum(Production.bags_60kg).label("total_bags"))
        .join(Production, Country.id == Production.country_id)
        .where(Production.year == latest_year)
        .group_by(Country.name)
        .order_by(func.sum(Production.bags_60kg).desc())
        .limit(1)
    )
    top_result = await db.execute(top_query)
    top_row = top_result.first()

    return OverviewResponse(
        total_countries=country_count,
        latest_year=latest_year,
        total_production_bags=total_bags,
        top_producer=top_row[0] if top_row else "N/A",
        top_producer_bags=float(top_row[1]) if top_row else 0,
    )
