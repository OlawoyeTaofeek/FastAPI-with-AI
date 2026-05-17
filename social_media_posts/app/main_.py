from fastapi import FastAPI
from . import models  
from .database import engine
from routers import posts, users, authentication, likes, comments
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(likes.router)
app.include_router(comments.router)
