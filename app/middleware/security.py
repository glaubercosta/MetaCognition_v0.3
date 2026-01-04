from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response

# Initialize the limiter with the client's IP address as the key
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def get_limiter():
    return limiter

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Custom handler for rate limit exceeded errors.
    Returns a JSON response with a 429 status code and a helpful message.
    """
    return _rate_limit_exceeded_handler(request, exc)
