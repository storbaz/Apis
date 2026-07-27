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


@router.get("/shared/{itinerary_id}")
async def get_shared_itinerary(itinerary_id: str):
    result = supabase.table("itineraries").select("*, users(name)").eq("id", itinerary_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return result.data[0]


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


@router.post("/{itinerary_id}/generate")
async def generate_itinerary(itinerary_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("itineraries").select("*").eq("id", itinerary_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    itin = existing.data[0]

    from datetime import datetime
    start = datetime.strptime(itin["start_date"], "%Y-%m-%d")
    end = datetime.strptime(itin["end_date"], "%Y-%m-%d")
    days = (end - start).days + 1

    day_templates = [
        "Llegada y check-in",
        "Explorar la ciudad",
        "Templo/Santuario principal",
        "Barrio comercial y compras",
        "Experiencia cultural",
        "Comida local recomendada",
        "Paseo nocturno",
        "Ultimo dia: souvenirs y despedida",
    ]

    supabase.table("itinerary_items").delete().eq("itinerary_id", itinerary_id).execute()

    items = []
    for d in range(1, min(days, 8) + 1):
        item = {
            "id": str(uuid.uuid4()),
            "itinerary_id": itinerary_id,
            "day_number": d,
            "time": "09:00",
            "title": day_templates[d - 1] if d - 1 < len(day_templates) else f"Dia {d}",
            "description": "",
            "location": "",
            "category": "general",
        }
        items.append(item)

    if items:
        supabase.table("itinerary_items").insert(items).execute()

    result_items = supabase.table("itinerary_items").select("*").eq("itinerary_id", itinerary_id).order("day_number").order("time").execute()
    return {**itin, "items": result_items.data}


@router.put("/{itinerary_id}/share")
async def toggle_share(itinerary_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("itineraries").select("is_shared").eq("id", itinerary_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    new_state = not existing.data[0].get("is_shared", False)
    supabase.table("itineraries").update({"is_shared": new_state}).eq("id", itinerary_id).execute()
    return {"is_shared": new_state}
