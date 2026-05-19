from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class PostBase(BaseModel):
    author: str = Field(..., example="Jane Doe")
    title: str = Field(..., example="Python is Great for Web Development")
    content: str = Field(..., example="Python is a great language for web development, and FastAPI makes it even better.", min_length=1, max_length=500)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    date_posted: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "author": "Jane Doe",
                "title": "Python is Great for Web Development",
                "content": "Python is a great language for web development, and FastAPI makes it even better.",
                "date_posted": "2021-01-03"
            }
        }
    )