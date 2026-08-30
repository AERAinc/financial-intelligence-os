from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.schemas.tenant import TenantCreate, TenantRead
from apps.api.app.services.tenant import TenantService
from core.db.session import get_db
from core.security.security import security_scheme
from core.tenancy.context import get_current_tenant_id

router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.post("", response_model=TenantRead, status_code=201)
async def create_tenant(
    data: TenantCreate,
    db: AsyncSession = Depends(get_db),
):
    service = TenantService(db)
    return await service.create_tenant(data)


@router.get("", response_model=list[TenantRead], dependencies=[Depends(security_scheme)])
async def list_tenants(
    db: AsyncSession = Depends(get_db),
    current_tenant_id: str = Depends(get_current_tenant_id),
):
    service = TenantService(db)
    return await service.list_tenants(tenant_id=current_tenant_id)