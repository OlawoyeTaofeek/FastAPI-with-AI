from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import List
import numpy as np 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class PostCreate(PostBase):
    pass

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    # embedding: List[float]
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)

class PostResponseLike(PostBase):
    id: int
    created_at: datetime
    user_id: int
    # embedding: List[float]
    owner: UserOut
    likes: int

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class PostsResponse(BaseModel):
    data: List[PostResponse]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class LikeCreate(BaseModel):
    post_id: int   
    direction: int = Field(..., ge=0, le=1, description="1 to like, 0 to unlike")

class LikeResponse(LikeCreate):
    user_id: int
 
    model_config = ConfigDict(from_attributes=True)
    
class CommentCreate(BaseModel):
    content: str

class ReplyCreate(BaseModel):
    content: str

class ReplyResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    comment_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    post_id: int
    owner: UserOut
    replies: List[ReplyResponse] = []

    model_config = ConfigDict(from_attributes=True)
    
  
class CommentOut(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True

class PostWithCommentsOut(BaseModel):
    id: int
    title: str
    likes: int
    comments: list[CommentOut]

    class Config:
        from_attributes = True
