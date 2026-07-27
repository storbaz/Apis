from fastapi import APIRouter, HTTPException, Depends
from app.core.security import get_current_user
from app.core.database import supabase
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(prefix="/community-tips", tags=["community-tips"])


class TipCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = "general"
    city: Optional[str] = ""
    tags: Optional[str] = ""


@router.get("")
async def list_tips():
    result = supabase.table("community_tips").select("*, users(name)").eq("approved", True).order("created_at", desc=True).limit(50).execute()
    return {"tips": result.data or []}


@router.get("/recent")
async def get_recent_tips():
    result = supabase.table("community_tips").select("*, users(name)").eq("approved", True).order("created_at", desc=True).limit(5).execute()
    return {"tips": result.data or []}


@router.post("")
async def create_tip(tip: TipCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    result = supabase.table("community_tips").insert({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "title": tip.title,
        "content": tip.content,
        "category": tip.category,
        "city": tip.city,
        "tags": tip.tags,
        "approved": True,
        "likes": 0,
    }).execute()

    return result.data[0]


@router.post("/{tip_id}/like")
async def like_tip(tip_id: str):
    existing = supabase.table("community_tips").select("likes").eq("id", tip_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Tip not found")

    current_likes = existing.data[0].get("likes", 0) or 0
    supabase.table("community_tips").update({"likes": current_likes + 1}).eq("id", tip_id).execute()
    return {"likes": current_likes + 1}


@router.delete("/{tip_id}")
async def delete_tip(tip_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("community_tips").select("id").eq("id", tip_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Tip not found")

    supabase.table("community_tips").delete().eq("id", tip_id).execute()
    return {"message": "Deleted"}
