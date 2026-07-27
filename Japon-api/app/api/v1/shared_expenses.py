from fastapi import APIRouter, HTTPException, Depends
from app.core.security import get_current_user
from app.core.database import supabase
from pydantic import BaseModel
from typing import Optional, List
import uuid

router = APIRouter(prefix="/shared-expenses", tags=["shared-expenses"])


class ExpenseGroupCreate(BaseModel):
    name: str
    description: Optional[str] = ""


class ExpenseCreate(BaseModel):
    group_id: str
    amount: float
    currency: Optional[str] = "JPY"
    description: str
    paid_by: Optional[str] = ""
    split_with: Optional[List[str]] = []


@router.post("/groups")
async def create_group(group: ExpenseGroupCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id, name").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    group_id = str(uuid.uuid4())
    result = supabase.table("expense_groups").insert({
        "id": group_id,
        "user_id": user_id,
        "name": group.name,
        "description": group.description,
    }).execute()

    supabase.table("expense_group_members").insert({
        "id": str(uuid.uuid4()),
        "group_id": group_id,
        "user_id": user_id,
        "name": user_result.data[0].get("name", "Yo"),
    }).execute()

    return result.data[0]


@router.get("/groups")
async def list_groups(current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    memberships = supabase.table("expense_group_members").select("group_id").eq("user_id", user_id).execute()
    group_ids = [m["group_id"] for m in (memberships.data or [])]

    if not group_ids:
        return {"groups": []}

    result = supabase.table("expense_groups").select("*").in_("id", group_ids).order("created_at", desc=True).execute()
    return {"groups": result.data}


@router.get("/groups/{group_id}")
async def get_group(group_id: str, current_user: dict = Depends(get_current_user)):
    result = supabase.table("expense_groups").select("*").eq("id", group_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Group not found")

    members = supabase.table("expense_group_members").select("*").eq("group_id", group_id).execute()
    expenses = supabase.table("expenses").select("*, users(name)").eq("group_id", group_id).order("created_at", desc=True).execute()

    return {**result.data[0], "members": members.data, "expenses": expenses.data}


@router.post("/groups/{group_id}/members")
async def add_member(group_id: str, name: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")

    result = supabase.table("expense_group_members").insert({
        "id": str(uuid.uuid4()),
        "group_id": group_id,
        "user_id": user_result.data[0]["id"],
        "name": name,
    }).execute()

    return result.data[0]


@router.post("/expenses")
async def add_expense(expense: ExpenseCreate, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    result = supabase.table("expenses").insert({
        "id": str(uuid.uuid4()),
        "group_id": expense.group_id,
        "user_id": user_id,
        "amount": expense.amount,
        "currency": expense.currency,
        "description": expense.description,
        "paid_by": expense.paid_by,
        "split_with": expense.split_with,
    }).execute()

    return result.data[0]


@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str, current_user: dict = Depends(get_current_user)):
    user_result = supabase.table("users").select("id").eq("email", current_user["sub"]).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user_result.data[0]["id"]

    existing = supabase.table("expenses").select("id").eq("id", expense_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Expense not found")

    supabase.table("expenses").delete().eq("id", expense_id).execute()
    return {"message": "Deleted"}


@router.get("/groups/{group_id}/balance")
async def get_balance(group_id: str, current_user: dict = Depends(get_current_user)):
    members = supabase.table("expense_group_members").select("*").eq("group_id", group_id).execute()
    expenses = supabase.table("expenses").select("*").eq("group_id", group_id).execute()

    member_list = members.data or []
    expense_list = expenses.data or []

    balances = {}
    for m in member_list:
        balances[m["name"]] = 0.0

    for e in expense_list:
        payer = e.get("paid_by", "")
        amount = e.get("amount", 0)
        split = e.get("split_with", [])

        if payer in balances:
            balances[payer] += amount

        if split and len(split) > 0:
            share = amount / len(split)
            for s in split:
                if s in balances:
                    balances[s] -= share

    total = sum(balances.values())
    return {"balances": balances, "total": total}
