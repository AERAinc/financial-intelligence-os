from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    tenant_id: str


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    tenant_id: str
    is_active: bool

    class Config:
        from_attributes = True