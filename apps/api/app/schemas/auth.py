from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    tenant_name: str = Field(..., example="Acme Corp")
    tenant_slug: str = Field(..., example="acme")
    email: EmailStr = Field(..., example="admin@acme.com")
    password: str = Field(..., min_length=8, example="Secret123!")
    full_name: str = Field(..., example="Admin User")  # <-- ADD THIS FIELD


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="admin@acme.com")
    password: str = Field(..., example="Secret123!")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    tenant_id: str
    email: str
    role: Optional[str] = "admin"

    class Config:
        from_attributes = True