from fastapi import APIRouter, Depends, status, Response, HTTPException
from app import models, utils
from app.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from app.schema import Token, UserOut
from app.models import User
from oauth2 import create_access_token, get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # NB: user)credentials returns 2 things: username and password
    db_user = db.query(models.User)\
                 .filter(models.User.email == user_credentials.username)\
                 .first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utils.verify_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    ## Create Token and the return the token
    access_token = create_access_token(
            data = {
                "user_id": db_user.id,
                "sub": db_user.email
            }
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=UserOut)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user