from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from app.schema import TokenData
from app.database import get_db
from typing import Annotated
from fastapi import HTTPException, status
from sqlalchemy.orm import Session  
from app.models import User
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
           minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception
    
def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], 
        db: Session = Depends(get_db)
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(
            token,
            credentials_exception=credentials_exception
    )

    user = db.query(User).filter(
        User.email == token_data.username
    ).first()

    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

                            


    

