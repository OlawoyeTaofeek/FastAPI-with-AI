from typing import Optional
from datetime import datetime, timedelta, timezone
from config import settings
from app.services.auth.schemas import TokenPayload, TokenType
from uuid import uuid4
from jose import jwt, JWTError

# ================================================================
# CUSTOM EXCEPTIONS
# Granular errors — routes know exactly what went wrong
# ================================================================
class TokenExpiredError(Exception):
    """Token signature is valid but it has expired"""
    pass
 
class TokenInvalidError(Exception):
    """Token is malformed, tampered with, or signature failed"""
    pass
 
class TokenTypeMismatchError(Exception):
    """Wrong token type used — e.g. refresh token used as access token"""
    pass
 
 
# ================================================================
# CREATE ACCESS TOKEN
# ================================================================
def create_access_token(
    user_id: str,
    email: str,
    role: str = "user",
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Creates a signed JWT access token.
 
    Args:
        user_id : The user's UUID from the database
        email   : User's email address
        role    : User's role — "user" or "admin"
        expires_delta : Override default expiry (useful for tests)
 
    Returns:
        Signed JWT string
    """
 
    now = datetime.now(timezone.utc)
 
    expire = now + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
 
    payload = {
        "sub": str(user_id),        
        "email": email,
        "role": role,
        "type": TokenType.ACCESS,
        "jti": str(uuid4()),   # unique token ID — for revocation if needed
        "iat": now,
        "exp": expire,
    }
 
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
 
    return token
 
 
# ================================================================
# VERIFY ACCESS TOKEN
# ================================================================
def verify_access_token(token: str) -> TokenPayload:
    """
    Decodes and fully validates a JWT access token.
 
    Validates:
        ✓ Signature (was it signed by us?)
        ✓ Expiry (has it expired?)
        ✓ Token type (is it actually an access token?)
        ✓ Required fields (sub, email, role all present?)
 
    Args:
        token : Raw JWT string from Authorization header
 
    Returns:
        TokenPayload — validated, typed payload
 
    Raises:
        TokenExpiredError       — token has expired
        TokenTypeMismatchError  — not an access token
        TokenInvalidError       — anything else wrong
    """
 
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],  # list — never a single string
            options={
                "verify_exp": True,           # always verify expiry
                "verify_iat": True,           # verify issued-at
                "require": [                  # these claims MUST be present
                    "sub",
                    "email",
                    "role",
                    "type",
                    "jti",
                    "iat",
                    "exp",
                ],
            },
        )
 
    except ExpiredSignatureError:
        # Separate from invalid — client needs to know to use refresh token
        raise TokenExpiredError("Access token has expired")
 
    except JWTError:
        # Covers: bad signature, malformed token, missing required claims
        raise TokenInvalidError("Access token is invalid")
 
    # ── Type check ────────────────────────────────────────────
    # Must happen AFTER decoding — type is inside the payload
    if payload.get("type") != TokenType.ACCESS:
        raise TokenTypeMismatchError(
            f"Expected access token, got: {payload.get('type')}"
        )
    
    try:
        return TokenPayload(**payload)
    except Exception:
        raise TokenInvalidError("Access token payload is malformed")