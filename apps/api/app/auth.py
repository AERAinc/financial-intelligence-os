import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.models.user import User
from apps.api.app.schemas.user import UserCreate
from core.security import create_access_token, hash_password, verify_password

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, data: UserCreate) -> User:
        stmt = select(User).where(User.email == data.email)
        existing = await self.db.scalar(stmt)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            id=str(uuid.uuid4()),
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            tenant_id=data.tenant_id,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate_user(self, email: str, password: str) -> dict:
        stmt = select(User).where(User.email == email)
        user = await self.db.scalar(stmt)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Token payload contains sub (user id) and tenant_id
        token_payload = {"sub": user.id, "tenant_id": user.tenant_id}
        token = create_access_token(token_payload)

        return {"access_token": token, "token_type": "bearer"}