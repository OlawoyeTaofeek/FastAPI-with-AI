from datetime import datetime, UTC, timedelta
from jose import jwt, JWTError
from .schema import TokenData
from .config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a signed JWT access token.

    - Copies the payload, then appends an expiry (`exp`) claim.
    - Falls back to `access_token_expire_minutes` from settings if no
      custom expiry is provided.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        key=settings.secret_key.get_secret_value(),  # ✅ consistent — SecretStr
        algorithm=settings.algorithm,                 # ✅ lowercase, matches config
    )


def verify_access_token(token: str, credentials_exception: Exception) -> TokenData:
    """
    Decode and validate a JWT access token.

    - Extracts the `sub` claim (email or username) as TokenData.
    - Raises `credentials_exception` if the token is missing, expired,
      invalid, or has no `sub` claim.
    """
    try:
        payload = jwt.decode(
            token=token,
            key=settings.secret_key.get_secret_value(),  # ✅ consistent — SecretStr
            algorithms=[settings.algorithm],              # ✅ lowercase, matches config
        )
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

        return TokenData(username=username)

    except JWTError:  # ✅ covers ALL jose exceptions — no second except needed
        raise credentials_exception