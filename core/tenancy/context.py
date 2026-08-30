from fastapi import Depends, HTTPException, status
from core.security.security import decode_access_token, security_scheme


async def get_current_tenant_id(credentials=Depends(security_scheme)) -> str:
    """Extracts tenant_id from JWT payload to enforce multi-tenant isolation."""
    # HTTPBearer returns an HTTPAuthorizationCredentials object containing credentials.credentials (the raw JWT string)
    payload = decode_access_token(credentials.credentials)
    if not payload or "tenant_id" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload["tenant_id"]