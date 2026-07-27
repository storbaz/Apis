from fastapi import APIRouter, HTTPException, Depends
from app.core.security import get_current_user
from app.core.database import supabase
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(prefix="/reviews", tags=["reviews"])


class ReviewCreate(BaseModel):
    itinerary_id: str
    rating: int
    comment: Optional[str] = ""


@router.get("/itinerary/{itinerary_id}")
async def get_reviews(itinerary_id: str):
    result = supabase.table("reviews").select("*, users(name)").eq("itinerary_id", itinerary_id).order("created_at", desc=True).execute()
    reviews = result.data or []
    avg = 0
    if reviews:
        avg = round(sum(r["rating"] for r in reviews) / len(reviews), 1)
    return {"reviews": reviews, "average": avg, "count": len(reviews)}


@router.post("")
async def create_review(review: ReviewCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("reviews").select("id").eq("itinerary_id", review.itinerary_id).eq("user_id", user_id).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Ya has valorado este itinerario")

    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="La valoracion debe ser entre 1 y 5")

    result = supabase.table("reviews").insert({
        "id": str(uuid.uuid4()),
        "itinerary_id": review.itinerary_id,
        "user_id": user_id,
        "rating": review.rating,
        "comment": review.comment,
    }).execute()

    return result.data[0]


@router.delete("/{review_id}")
async def delete_review(review_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("reviews").select("id").eq("id", review_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Review not found")

    supabase.table("reviews").delete().eq("id", review_id).execute()
    return {"message": "Deleted"}


@router.get("/recent")
async def get_recent_reviews():
    result = supabase.table("reviews").select("*, users(name), itineraries(title)").order("created_at", desc=True).limit(10).execute()
    return {"reviews": result.data or []}
