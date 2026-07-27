from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, ApiKey, PLAN_RATE_LIMITS
from app.schemas.api_key import ApiKeyCreate, ApiKeyResponse, ApiKeyListResponse
from app.services.email_service import send_api_key_email

router = APIRouter(prefix="/api-keys", tags=["api-keys"])


@router.get("", response_model=ApiKeyListResponse)
async def list_keys(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ApiKey).where(ApiKey.user_id == user.id).order_by(ApiKey.created_at.desc())
    )
    keys = result.scalars().all()
    return ApiKeyListResponse(keys=keys, total=len(keys))


@router.post("", response_model=ApiKeyResponse, status_code=201)
async def create_key(
    body: ApiKeyCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rate_limit = PLAN_RATE_LIMITS.get(user.plan, 100)
    key = ApiKey(
        user_id=user.id,
        name=body.name,
        rate_limit=rate_limit if rate_limit != -1 else 999999,
    )
    db.add(key)
    await db.commit()
    await db.refresh(key)

    send_api_key_email(
        user.email,
        user.full_name or user.email,
        body.name,
        key.key,
    )

    return key


@router.delete("/{key_id}", status_code=204)
async def revoke_key(
    key_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ApiKey).where(ApiKey.id == key_id, ApiKey.user_id == user.id)
    )
    key = result.scalar_one_or_none()

    if not key:
        raise HTTPException(status_code=404, detail="API key not found")

    await db.delete(key)
    await db.commit()
