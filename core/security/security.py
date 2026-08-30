from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

SECRET_KEY = "DEV_SECRET_KEY_CHANGE_IN_PRODUCTION_ENV"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# HTTPBearer creates a simple Token input box in Swagger UI
security_scheme = HTTPBearer()

def hash_password(plain_password: str) -> str:
    pwd_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hash_bytes)

def create_access_token(user_id: str, tenant_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id),
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

class TenantSecurityManager:
    """Enforces multi-tenant isolation rules and security validations."""

    @staticmethod
    def verify_tenant_access(
        requested_tenant_id: str, 
        current_tenant_id: str = Depends(lambda: __import__('core.tenancy.context', fromlist=['get_current_tenant_id']).get_current_tenant_id())
    ) -> bool:
        if not current_tenant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tenant context missing from authorization headers."
            )
        if requested_tenant_id != current_tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cross-tenant access violation detected and blocked."
            )
        return True

tenant_security = TenantSecurityManager()