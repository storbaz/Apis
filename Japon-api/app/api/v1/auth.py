from fastapi import APIRouter, HTTPException, Depends
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.database import supabase
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["authentication"])

class UserRegister(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user: UserRegister):
    existing = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    result = supabase.table("users").insert({
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
    if not verify_password(user.password, stored_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email, "plan": stored_user["plan"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": user.email, "name": stored_user["name"], "plan": stored_user["plan"]}
    }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    result = supabase.table("users").select("email,name,plan").eq("email", current_user["sub"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    return result.data[0]