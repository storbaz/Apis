from fastapi import APIRouter, HTTPException, Depends
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.database import supabase
from pydantic import BaseModel
from typing import Optional
import uuid
import httpx

router = APIRouter(prefix="/auth", tags=["authentication"])

class UserRegister(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class GoogleLogin(BaseModel):
    id_token: str

class ProfileUpdate(BaseModel):
    name: Optional[str] = None


def get_or_create_user(email: str, name: str, provider: str = "email") -> dict:
    existing = supabase.table("users").select("*").eq("email", email).execute()
    if existing.data:
        return existing.data[0]

    result = supabase.table("users").insert({
        "id": str(uuid.uuid4()),
        "email": email,
        "name": name,
        "password_hash": "",
        "plan": "free",
    }).execute()
    return result.data[0]


@router.post("/register")
async def register(user: UserRegister):
    existing = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    result = supabase.table("users").insert({
        "id": str(uuid.uuid4()),
        "email": user.email,
        "name": user.name,
        "password_hash": hash_password(user.password),
        "plan": "free"
    }).execute()

    token = create_access_token(data={"sub": user.email, "plan": "free"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": user.email, "name": user.name, "plan": "free"}
    }


@router.post("/login")
async def login(user: UserLogin):
    result = supabase.table("users").select("*").eq("email", user.email).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_user = result.data[0]
    if not stored_user.get("password_hash") or not verify_password(user.password, stored_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email, "plan": stored_user["plan"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": user.email, "name": stored_user["name"], "plan": stored_user["plan"]}
    }


@router.post("/google")
async def google_login(data: GoogleLogin):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": data.id_token}, timeout=10.0)
            if resp.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid Google token")
            google_user = resp.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Could not verify Google token")

    email = google_user.get("email")
    name = google_user.get("name", email.split("@")[0])

    if not email:
        raise HTTPException(status_code=401, detail="No email in Google token")

    user = get_or_create_user(email, name, "google")
    token = create_access_token(data={"sub": email, "plan": user.get("plan", "free")})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": email, "name": user["name"], "plan": user.get("plan", "free")}
    }


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    result = supabase.table("users").select("email,name,plan").eq("email", current_user["sub"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    return result.data[0]


@router.put("/me")
async def update_me(profile: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    updates = {}
    if profile.name is not None:
        updates["name"] = profile.name

    if updates:
        supabase.table("users").update(updates).eq("email", current_user["sub"]).execute()

    result = supabase.table("users").select("email,name,plan").eq("email", current_user["sub"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    return result.data[0]


class DeleteAccountRequest(BaseModel):
    email: str
    password: str


@router.delete("/delete-account")
async def delete_account(body: DeleteAccountRequest, current_user: dict = Depends(get_current_user)):
    email = current_user["sub"]

    user_result = supabase.table("users").select("*").eq("email", email).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")

    stored_user = user_result.data[0]
    if not stored_user.get("password_hash") or not verify_password(body.password, stored_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    tables_to_clean = [
        ("itineraries", "user_email"),
        ("shopping_lists", "user_email"),
        ("shopping_items", "list_id"),
        ("community_tips", "user_email"),
        ("reviews", "user_email"),
        ("expense_groups", "user_email"),
        ("favorites", "user_email"),
    ]

    for table, column in tables_to_clean:
        try:
            if column == "user_email":
                supabase.table(table).delete().eq(column, email).execute()
            elif table == "shopping_items":
                lists = supabase.table("shopping_lists").select("id").eq("user_email", email).execute()
                for lst in (lists.data or []):
                    supabase.table(table).delete().eq("list_id", lst["id"]).execute()
        except Exception:
            pass

    supabase.table("users").delete().eq("email", email).execute()

    return {"message": "Account and all data deleted permanently"}
