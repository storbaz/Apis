from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.deps import get_api_key_owner
from app.models.coffee import Export, Country
from app.models.user import User
from app.schemas.production import ProductionResponse

router = APIRouter(dependencies=[Depends(get_api_key_owner)])


@router.get("/exports")
async def get_exports(
    country: str = Query(None, description="Origin country code or name"),
    destination: str = Query(None, description="Destination country code or name"),
    year_from: int = Query(None, ge=1961),
    year_to: int = Query(None, le=2030),
    hs_code: str = Query(None, description="HS code (e.g. 090111)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_api_key_owner),
):
    query = (
        select(Export, Country.label("origin"), Country.label("dest"))
        .join(Country, Export.country_id == Country.id)
    )

    if country:
        query = query.where(
            (Country.code.ilike(f"%{country}%")) | (Country.name.ilike(f"%{country}%"))
        )
    if year_from:
        query = query.where(Export.year >= year_from)
    if year_to:
        query = query.where(Export.year <= year_to)
    if hs_code:
        query = query.where(Export.hs_code == hs_code)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Export.year.desc(), Country.name)
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)

    data = []
    for row in result.all():
        e = row[0]
        origin = row[1]
        data.append({
            "origin_country": origin.name,
            "origin_code": origin.code,
            "year": e.year,
            "month": e.month,
            "hs_code": e.hs_code,
            "bags_60kg": float(e.bags_60kg) if e.bags_60kg else None,
            "tonnes": float(e.tonnes) if e.tonnes else None,
            "value_usd": float(e.value_usd) if e.value_usd else None,
            "source": e.source,
        })

    return {
        "data": data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }
