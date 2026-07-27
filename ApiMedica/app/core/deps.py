from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.database import get_db
from app.models.user import User, ApiKey, PLAN_RATE_LIMITS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

RATE_LIMIT_STORAGE: dict[str, list[datetime]] = {}


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire},
        settings.JWT_SECRET,
        algorithm="HS256",
    )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid or inactive user")

    return user


async def get_api_key_owner(
    x_api_key: Optional[str] = Header(None),
    api_key: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    key_value = x_api_key or api_key
    if not key_value:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Pass X-API-Key header or ?api_key= query param.",
        )

    result = await db.execute(select(ApiKey).where(ApiKey.key == key_value, ApiKey.is_active == True))
    api_key_obj = result.scalar_one_or_none()

    if not api_key_obj:
        raise HTTPException(status_code=401, detail="Invalid or revoked API key")

    api_key_obj.last_used_at = datetime.utcnow()
    await db.commit()

    result = await db.execute(select(User).where(User.id == api_key_obj.user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="API key owner is inactive")

    rate_limit = PLAN_RATE_LIMITS.get(user.plan, 100)
    if rate_limit != -1:
        now = datetime.utcnow()
        key = f"{user.id}:{now.strftime('%Y-%m-%d')}"
        hits = RATE_LIMIT_STORAGE.get(key, [])
        hits = [t for t in hits if (now - t).total_seconds() < 86400]
        if len(hits) >= rate_limit:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded for {user.plan} plan ({rate_limit}/day).",
            )
        hits.append(now)
        RATE_LIMIT_STORAGE[key] = hits

    return user


async def get_optional_user(
    x_api_key: Optional[str] = Header(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    if credentials:
        try:
            payload = jwt.decode(credentials.credentials, settings.JWT_SECRET, algorithms=["HS256"])
            user_id = int(payload.get("sub"))
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user and user.is_active:
                return user
        except (JWTError, ValueError):
            pass

    if x_api_key:
        result = await db.execute(select(ApiKey).where(ApiKey.key == x_api_key, ApiKey.is_active == True))
        api_key_obj = result.scalar_one_or_none()
        if api_key_obj:
            result = await db.execute(select(User).where(User.id == api_key_obj.user_id))
            user = result.scalar_one_or_none()
            if user and user.is_active:
                return user

    return None
