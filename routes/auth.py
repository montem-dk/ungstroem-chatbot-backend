from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.supabase_client import DatabaseHandler

supabase = DatabaseHandler()

router = APIRouter(prefix="/auth", tags=["Auth"])

class AuthSchema(BaseModel):
    name: str = Field("Zohaib Munir")
    email: str = Field("zohaibmunir32@gmail.com")
    password: str = Field("aaaaaa")
    phone_number: str = Field("+923364359237", alias="phone")

@router.post("/register")
def register_user(auth: AuthSchema):
    try:
        return supabase.register_user(auth.name, auth.email, auth.password, auth.phone_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user(auth: AuthSchema):
    try:
        return supabase.login_user(auth.email, auth.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users")
def get_all_users():
    try:
        return supabase.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}")
def get_user_by_id(user_id: str):
    try:
        return supabase.get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update_user")
def update_user(user_id: str, data: AuthSchema):
    try:
        return supabase.update_user(
            user_id,
            data.email,
            data.name,
            data.phone_number,
            data.password
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete_user")
def delete_user(user_id: str):
    try:
        print("user id:", user_id)
        return supabase.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))