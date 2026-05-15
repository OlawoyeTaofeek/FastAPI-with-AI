from fastapi import status, Response, HTTPException, Depends, APIRouter
from app import models  
from typing import List, Optional
from app.database import get_db
from sqlalchemy.orm import Session
from app.schema import LikeResponse, LikeCreate
from oauth2 import get_current_user
from app.models import User
from sqlalchemy import and_, or_


router = APIRouter(prefix="/likes", tags=['likes'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(like: LikeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # check if the post exists first
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {like.post_id} not found")

    vote_query = db.query(models.Like).filter(
        models.Like.user_id == current_user.id,
        models.Like.post_id == like.post_id
    )
    existing = vote_query.first()

    if like.direction == 1:
        # like
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Post {like.post_id} already liked")
        new_like = models.Like(user_id=current_user.id, post_id=like.post_id)
        db.add(new_like)
        db.commit()
        return {"message": f"Post {like.post_id} liked successfully"}

    else:
        # unlike (direction == 0)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {like.post_id} has not been liked yet")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"Post {like.post_id} unliked successfully"}