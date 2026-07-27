from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.deps import get_api_key_owner
from app.models.coffee import Price
from app.models.user import User
from app.schemas.production import PriceResponse

router = APIRouter(dependencies=[Depends(get_api_key_owner)])


@router.get("/prices")
async def get_prices(
    variety: str = Query(None, description="arabica or robusta"),
    date_from: str = Query(None, description="YYYY-MM-DD"),
    date_to: str = Query(None, description="YYYY-MM-DD"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_api_key_owner),
):
    query = select(Price)

    if variety:
        query = query.where(Price.variety == variety)
    if date_from:
        query = query.where(Price.date >= date_from)
    if date_to:
        query = query.where(Price.date <= date_to)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Price.date.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)

    data = [
        PriceResponse(
            date=str(p.date),
            variety=p.variety,
            price_usd_cents_per_lb=float(p.price_usd_cents_per_lb),
            source=p.source,
        )
        for p in result.scalars().all()
    ]

    return {
        "data": data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/prices/latest")
async def get_latest_price(
    variety: str = Query("arabica", description="arabica or robusta"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_api_key_owner),
):
    query = (
        select(Price)
        .where(Price.variety == variety)
        .order_by(Price.date.desc())
        .limit(1)
    )
    result = await db.execute(query)
    price = result.scalar_one_or_none()

    if not price:
        return {"data": None, "message": f"No price data found for {variety}"}

    return {
        "data": PriceResponse(
            date=str(price.date),
            variety=price.variety,
            price_usd_cents_per_lb=float(price.price_usd_cents_per_lb),
            source=price.source,
        )
    }
