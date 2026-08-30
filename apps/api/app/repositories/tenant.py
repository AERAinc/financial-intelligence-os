from sqlalchemy.orm import Session
from apps.api.app.models.tenant import Tenant
from apps.api.app.schemas.tenant import TenantCreate
import uuid


class TenantRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: TenantCreate) -> Tenant:
        tenant = Tenant(
            id=uuid.uuid4(),
            name=data.name,
            slug=data.slug,
            is_active=True,
        )
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant

    def list_all(self) -> list[Tenant]:
        return self.db.query(Tenant).order_by(Tenant.created_at.desc()).all()

    def get_by_slug(self, slug: str) -> Tenant | None:
        return self.db.query(Tenant).filter(Tenant.slug == slug).first()