import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.models.tenant import Tenant
from apps.api.app.schemas.tenant import TenantCreate


class TenantService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tenant(self, data: TenantCreate) -> Tenant:
        payload = data.model_dump()
        
        # Ensure ID is generated if not set by model default
        if "id" not in payload or not payload["id"]:
            payload["id"] = str(uuid.uuid4())

        tenant = Tenant(**payload)
        self.db.add(tenant)
        await self.db.commit()
        await self.db.refresh(tenant)
        return tenant

    async def list_tenants(self, tenant_id: str | None = None) -> list[Tenant]:
        stmt = select(Tenant)
        if tenant_id:
            stmt = stmt.where(Tenant.id == tenant_id)
            
        result = await self.db.scalars(stmt)
        return list(result.all())