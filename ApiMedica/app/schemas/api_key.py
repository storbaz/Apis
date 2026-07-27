from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ApiKeyCreate(BaseModel):
    name: str


class ApiKeyResponse(BaseModel):
    id: int
    key: str
    name: str
    rate_limit: int
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]

    class Config:
        from_attributes = True


class ApiKeyListResponse(BaseModel):
    keys: List[ApiKeyResponse]
    total: int
