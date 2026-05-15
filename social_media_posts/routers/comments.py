from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app import models
from app.database import get_db
from app.schema import CommentCreate, CommentResponse, ReplyCreate, ReplyResponse
from app.models import User
from oauth2 import get_current_user
from typing import List

router = APIRouter(prefix="/comments", tags=['Comments'])

# Create a comment on a post
@router.post("/{post_id}", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} doesn't exists")
    
    post_comment = models.Comment(**comment.model_dump(), post_id=post_id, user_id=user.id) 
    db.add(post_comment)
    db.commit()
    db.refresh(post_comment)
    return post_comment  

# get all comments for a post
@router.get("/{post_id}", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    
    query = db.query(models.Comment).filter(models.Comment.post_id == post_id) \
              .options(joinedload(models.Comment.replies)).all()
    
    return query

# delete a comment
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id,
        models.Comment.user_id == user.id

    ).first()
    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment_id} not found")

    db.delete(comment)
    db.commit()

# reply to a comment
@router.post("/{comment_id}/replies", response_model=ReplyResponse, status_code=status.HTTP_201_CREATED)
def create_reply(comment_id: int, reply: ReplyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment_id} not found")

    new_reply = models.Reply(
        content=reply.content,
        comment_id=comment_id,
        user_id=current_user.id
    )
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply

## get reply
@router.get("/{comment_id}/replies", response_model=List[ReplyResponse], status_code=status.HTTP_200_OK)
def get_replies(comment_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Check if comment exists
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment_id} not found")
    
    query = db.query(models.Reply).filter(
        models.Reply.comment_id == comment_id
    ).outerjoin(models.User, models.Reply.user_id == models.User.id).all()
    print(query)
    
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No replies found for comment {comment_id}")
    return query

# delete a reply
@router.delete("/replies/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reply(reply_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reply = db.query(models.Reply).filter(
        models.Reply.id == reply_id,
        models.Reply.user_id == current_user.id
    ).first()

    if not reply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reply {reply_id} not found")

    db.delete(reply)
    db.commit()