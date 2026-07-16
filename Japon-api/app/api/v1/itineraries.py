from fastapi import APIRouter, HTTPException, Depends
from app.core.security import get_current_user
from app.core.database import supabase
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(prefix="/itineraries", tags=["itineraries"])


class ItineraryCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    start_date: str
    end_date: str


class ItineraryItemCreate(BaseModel):
    day_number: int
    time: Optional[str] = ""
    title: str
    description: Optional[str] = ""
    location: Optional[str] = ""
    category: Optional[str] = ""


@router.get("")
async def list_itineraries(current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    result = supabase.table("itineraries").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return {"itineraries": result.data}


@router.post("")
async def create_itinerary(itin: ItineraryCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    result = supabase.table("itineraries").insert({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "title": itin.title,
        "description": itin.description,
        "start_date": itin.start_date,
        "end_date": itin.end_date,
    }).execute()

    return result.data[0]


@router.get("/{itinerary_id}")
async def get_itinerary(itinerary_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    result = supabase.table("itineraries").select("*").eq("id", itinerary_id).eq("user_id", user_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    items = supabase.table("itinerary_items").select("*").eq("itinerary_id", itinerary_id).order("day_number").order("time").execute()

    return {**result.data[0], "items": items.data}


@router.put("/{itinerary_id}")
async def update_itinerary(itinerary_id: str, itin: ItineraryCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("itineraries").select("*").eq("id", itinerary_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    result = supabase.table("itineraries").update({
        "title": itin.title,
        "description": itin.description,
        "start_date": itin.start_date,
        "end_date": itin.end_date,
    }).eq("id", itinerary_id).execute()

    return result.data[0]


@router.delete("/{itinerary_id}")
async def delete_itinerary(itinerary_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("itineraries").select("*").eq("id", itinerary_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    supabase.table("itinerary_items").delete().eq("itinerary_id", itinerary_id).execute()
    supabase.table("itineraries").delete().eq("id", itinerary_id).execute()
    return {"message": "Deleted"}


@router.post("/{itinerary_id}/items")
async def add_item(itinerary_id: str, item: ItineraryItemCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("itineraries").select("*").eq("id", itinerary_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    result = supabase.table("itinerary_items").insert({
        "id": str(uuid.uuid4()),
        "itinerary_id": itinerary_id,
        "day_number": item.day_number,
        "time": item.time,
        "title": item.title,
        "description": item.description,
        "location": item.location,
        "category": item.category,
    }).execute()

    return result.data[0]


@router.delete("/{itinerary_id}/items/{item_id}")
async def remove_item(itinerary_id: str, item_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("itineraries").select("*").eq("id", itinerary_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    supabase.table("itinerary_items").delete().eq("id", item_id).eq("itinerary_id", itinerary_id).execute()
    return {"message": "Removed"}
