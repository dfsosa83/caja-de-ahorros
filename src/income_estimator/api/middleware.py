"""
Custom middleware for the Income Estimator ML API.
"""

import time
from typing import Dict

from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..logger import get_logger

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware to prevent API abuse."""
    
    def __init__(self, app, requests_per_minute: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = window_seconds
        self.request_counts: Dict[str, Dict[str, int]] = {}
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        client_ip = self._get_client_ip(request)
        current_time = int(time.time())
        window_start = current_time - (current_time % self.window_seconds)
        
        # Initialize client tracking if not exists
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {}
        
        # Clean old windows
        self._clean_old_windows(client_ip, window_start)
        
        # Check current window
        if window_start not in self.request_counts[client_ip]:
            self.request_counts[client_ip][window_start] = 0
        
        # Check rate limit
        if self.request_counts[client_ip][window_start] >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": str(self.window_seconds)}
            )
        
        # Increment counter
        self.request_counts[client_ip][window_start] += 1
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.requests_per_minute - self.request_counts[client_ip][window_start])
        )
        response.headers["X-RateLimit-Reset"] = str(window_start + self.window_seconds)
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request."""
        # Check for forwarded headers (when behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"
    
    def _clean_old_windows(self, client_ip: str, current_window: int):
        """Remove old time windows to prevent memory leaks."""
        cutoff_time = current_window - (self.window_seconds * 2)  # Keep 2 windows
        
        windows_to_remove = [
            window for window in self.request_counts[client_ip]
            if window < cutoff_time
        ]
        
        for window in windows_to_remove:
            del self.request_counts[client_ip][window]


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next):
        """Add security headers to response."""
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Validate incoming requests for common issues."""
    
    def __init__(self, app, max_request_size: int = 10 * 1024 * 1024):  # 10MB
        super().__init__(app)
        self.max_request_size = max_request_size
    
    async def dispatch(self, request: Request, call_next):
        """Validate request before processing."""
        # Check request size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_request_size:
            logger.warning(f"Request too large: {content_length} bytes")
            raise HTTPException(
                status_code=413,
                detail="Request entity too large"
            )
        
        # Check content type for POST requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if not content_type.startswith("application/json"):
                if request.url.path not in ["/docs", "/redoc", "/openapi.json"]:
                    logger.warning(f"Invalid content type: {content_type}")
                    raise HTTPException(
                        status_code=415,
                        detail="Unsupported media type. Expected application/json"
                    )
        
        return await call_next(request)
