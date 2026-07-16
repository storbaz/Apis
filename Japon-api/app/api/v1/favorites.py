from fastapi import APIRouter, HTTPException, Depends
from app.core.security import get_current_user
from app.core.database import supabase
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(prefix="/favorites", tags=["favorites"])


class FavoriteCreate(BaseModel):
    item_type: str
    item_id: str


@router.get("")
async def list_favorites(current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    result = supabase.table("favorites").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return {"favorites": result.data}


@router.post("")
async def add_favorite(fav: FavoriteCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("favorites").select("*").eq("user_id", user_id).eq("item_type", fav.item_type).eq("item_id", fav.item_id).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Already in favorites")

    result = supabase.table("favorites").insert({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "item_type": fav.item_type,
        "item_id": fav.item_id,
    }).execute()

    return result.data[0]


@router.delete("/{favorite_id}")
async def remove_favorite(favorite_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("favorites").select("*").eq("id", favorite_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Favorite not found")

    supabase.table("favorites").delete().eq("id", favorite_id).execute()
    return {"message": "Removed"}
