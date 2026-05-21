from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from datetime import datetime
import re


# ─── User Schemas ─────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    username:  str      = Field(min_length=1, max_length=50)
    email:     EmailStr = Field(max_length=200)
    full_name: str      = Field(min_length=2, max_length=150)

class UserCreate(UserBase):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Must contain at least one special character")
        return value

class UserResponse(UserBase):
    id:         int
    image_file: str | None
    image_path: str          

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)


# ─── Post Schemas ─────────────────────────────────────────────────────────────

class PostCreate(BaseModel):
    title:   str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    user_id: int = Field(..., description="ID of the user creating the post")

class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)

class PostResponse(BaseModel):
    id:          int
    title:       str
    content:     str
    date_posted: datetime 
    user_id:     int  
    updated_at:  datetime
    author:      UserResponse 

    model_config = ConfigDict(from_attributes=True)

class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)