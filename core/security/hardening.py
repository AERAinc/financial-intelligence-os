from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class EnterpriseSecurityHardeningMiddleware(BaseHTTPMiddleware):
    """Adds enterprise-grade security and compliance headers to all HTTP responses, 
    with explicit exceptions for interactive documentation assets."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Allow Swagger UI/Redoc CDNs to load properly by relaxing CSP on docs endpoints
        path = request.url.path
        if path in ("/docs", "/redoc", "/openapi.json") or path.startswith("/docs/"):
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Content-Security-Policy"] = (
                "default-src 'self' 'unsafe-inline' 'unsafe-eval' "
                "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;"
            )
            return response

        # Standard strict security headers for all other application routes
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response