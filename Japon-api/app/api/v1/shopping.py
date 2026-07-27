from fastapi import APIRouter, HTTPException, Depends
from app.core.security import get_current_user
from app.core.database import supabase
from pydantic import BaseModel
from typing import Optional, List
import uuid

router = APIRouter(prefix="/shopping", tags=["shopping"])


class ShoppingListCreate(BaseModel):
    title: str
    trip_id: Optional[str] = None


class ShoppingItemCreate(BaseModel):
    name: str
    category: Optional[str] = "general"
    store: Optional[str] = ""
    quantity: Optional[int] = 1
    notes: Optional[str] = ""


class ShoppingItemUpdate(BaseModel):
    name: Optional[str] = None
    checked: Optional[bool] = None
    quantity: Optional[int] = None
    notes: Optional[str] = None
    store: Optional[str] = None


# ── Lists ──

@router.get("")
async def list_shopping_lists(current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    result = supabase.table("shopping_lists").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return {"lists": result.data}


@router.post("")
async def create_shopping_list(data: ShoppingListCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    list_id = str(uuid.uuid4())
    share_token = str(uuid.uuid4())[:8]

    result = supabase.table("shopping_lists").insert({
        "id": list_id,
        "user_id": user_id,
        "title": data.title,
        "trip_id": data.trip_id,
        "share_token": share_token,
    }).execute()

    return result.data[0]


@router.get("/{list_id}")
async def get_shopping_list(list_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    result = supabase.table("shopping_lists").select("*").eq("id", list_id).eq("user_id", user_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="List not found")

    items = supabase.table("shopping_items").select("*").eq("list_id", list_id).order("category").order("name").execute()

    return {**result.data[0], "items": items.data}


@router.delete("/{list_id}")
async def delete_shopping_list(list_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("shopping_lists").select("*").eq("id", list_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="List not found")

    supabase.table("shopping_items").delete().eq("list_id", list_id).execute()
    supabase.table("shopping_lists").delete().eq("id", list_id).execute()
    return {"message": "Deleted"}


# ── Items ──

@router.post("/{list_id}/items")
async def add_item(list_id: str, item: ShoppingItemCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("shopping_lists").select("*").eq("id", list_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="List not found")

    result = supabase.table("shopping_items").insert({
        "id": str(uuid.uuid4()),
        "list_id": list_id,
        "name": item.name,
        "category": item.category,
        "store": item.store,
        "quantity": item.quantity,
        "notes": item.notes,
    }).execute()

    return result.data[0]


@router.put("/{list_id}/items/{item_id}")
async def update_item(list_id: str, item_id: str, data: ShoppingItemUpdate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("shopping_lists").select("*").eq("id", list_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="List not found")

    updates = {}
    if data.name is not None:
        updates["name"] = data.name
    if data.checked is not None:
        updates["checked"] = data.checked
    if data.quantity is not None:
        updates["quantity"] = data.quantity
    if data.notes is not None:
        updates["notes"] = data.notes
    if data.store is not None:
        updates["store"] = data.store

    if updates:
        supabase.table("shopping_items").update(updates).eq("id", item_id).eq("list_id", list_id).execute()

    return {"message": "Updated"}


@router.delete("/{list_id}/items/{item_id}")
async def remove_item(list_id: str, item_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("shopping_lists").select("*").eq("id", list_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="List not found")

    supabase.table("shopping_items").delete().eq("id", item_id).eq("list_id", list_id).execute()
    return {"message": "Removed"}


# ── Public share ──

@router.get("/shared/{token}")
async def get_shared_list(token: str):
    result = supabase.table("shopping_lists").select("*, users(name)").eq("share_token", token).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="List not found")

    list_data = result.data[0]
    items = supabase.table("shopping_items").select("*").eq("list_id", list_data["id"]).order("category").order("name").execute()

    return {**list_data, "items": items.data}
