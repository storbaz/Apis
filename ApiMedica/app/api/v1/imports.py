from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.deps import get_api_key_owner
from app.models.coffee import Import, Country
from app.models.user import User

router = APIRouter(dependencies=[Depends(get_api_key_owner)])


@router.get("/imports")
async def get_imports(
    country: str = Query(None, description="Destination country code or name"),
    origin: str = Query(None, description="Origin country code or name"),
    year_from: int = Query(None, ge=1961),
    year_to: int = Query(None, le=2030),
    hs_code: str = Query(None, description="HS code (e.g. 090111)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_api_key_owner),
):
    query = (
        select(Import, Country.label("dest"), Country.label("origin"))
        .join(Country, Import.country_id == Country.id)
    )

    if country:
        query = query.where(
            (Country.code.ilike(f"%{country}%")) | (Country.name.ilike(f"%{country}%"))
        )
    if year_from:
        query = query.where(Import.year >= year_from)
    if year_to:
        query = query.where(Import.year <= year_to)
    if hs_code:
        query = query.where(Import.hs_code == hs_code)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Import.year.desc(), Country.name)
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)

    data = []
    for row in result.all():
        i = row[0]
        dest = row[1]
        data.append({
            "destination_country": dest.name,
            "destination_code": dest.code,
            "year": i.year,
            "month": i.month,
            "hs_code": i.hs_code,
            "bags_60kg": float(i.bags_60kg) if i.bags_60kg else None,
            "tonnes": float(i.tonnes) if i.tonnes else None,
            "value_usd": float(i.value_usd) if i.value_usd else None,
            "source": i.source,
        })

    return {
        "data": data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }
