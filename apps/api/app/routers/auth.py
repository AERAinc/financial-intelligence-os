import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.models.tenant import Tenant
from apps.api.app.models.user import User
from apps.api.app.schemas.auth import TokenResponse, UserCreate, UserLogin, UserResponse
from core.db.session import get_db
from core.security.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if tenant slug already exists
    existing_tenant = await db.scalar(select(Tenant).where(Tenant.slug == payload.tenant_slug))
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant slug already in use")

    # Check if user email already exists
    existing_user = await db.scalar(select(User).where(User.email == payload.email))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Provision tenant and admin user with explicit UUID string IDs
    tenant = Tenant(
        id=str(uuid.uuid4()),
        name=payload.tenant_name,
        slug=payload.tenant_slug,
    )
    db.add(tenant)
    await db.flush()

    user = User(
        id=str(uuid.uuid4()),
        tenant_id=tenant.id,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user_id=user.id, tenant_id=user.tenant_id)
    return TokenResponse(access_token=token)