from fastapi import status, Response, HTTPException, Depends, APIRouter
from app import models  
from app.database import get_db
from sqlalchemy.orm import Session
from app.schema import UserCreate, UserResponse, UserOut
from app import utils
from typing import List

router = APIRouter(
            prefix="/users",
            tags=["Users"]
        )

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    ## hash password 
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user
   
