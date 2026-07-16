from fastapi import APIRouter, Query, HTTPException
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from fastapi import Depends
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["authentication"])

USERS_DB = {}


class UserRegister(BaseModel):
    email: str
    password: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(user: UserRegister):
    if user.email in USERS_DB:
        raise HTTPException(status_code=400, detail="Email already registered")

    USERS_DB[user.email] = {
        "email": user.email,
        "name": user.name,
        "password": hash_password(user.password),
        "plan": "free",
        "created_at": "2024-01-01"
    }

    token = create_access_token(data={"sub": user.email, "plan": "free"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "name": user.name,
            "plan": "free"
        }
    }


@router.post("/login")
async def login(user: UserLogin):
    if user.email not in USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_user = USERS_DB[user.email]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email, "plan": stored_user["plan"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "name": stored_user["name"],
            "plan": stored_user["plan"]
        }
    }


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user_data = USERS_DB.get(current_user["sub"])
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "email": user_data["email"],
        "name": user_data["name"],
        "plan": user_data["plan"]
    }
