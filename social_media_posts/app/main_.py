from fastapi import FastAPI
from . import models  
from .database import engine
from routers import posts, users, authentication, likes, comments

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(likes.router)
app.include_router(comments.router)
