from fastapi import FastAPI, Request, status, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException # To return HTML responses
from fastapi.exceptions import RequestValidationError # To handle validation errors
from fastapi.responses import JSONResponse # To return JSON responses for errors
from .schema import PostCreate, PostResponse
from typing import List
from datetime import timezone, datetime
from .utils import format_date
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_
from . import models
from fastapi import Depends
from .database import Base, get_db, engine 
from typing import Annotated 
from .schema import (PostCreate, PostResponse, UserCreate, 
    UserResponse, PostUpdate, PostUpdate, UserUpdate)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")
templates.env.filters["format_date"] = format_date

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    posts = db.execute(
        select(models.Post).order_by(models.Post.date_posted.desc())
    ).scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"posts": posts}
    )


@app.get("/posts/{post_id}", include_in_schema=False, name="post")
def post_page(request: Request, post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return templates.TemplateResponse(
            request,
            "post.html",
            context= {
                "post": post,
                "title": post.title[:50]
            }
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )

@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):

    # existing_user = db.query(models.User).filter(
    #     (user.email == models.User.email) | user.username == models.User.username 
    # ).first() Old approach

    existing_user = db.execute(
        select(models.User).where(
            or_(user.email==models.User.email,
                models.User.username == user.username
            )
            
        )
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Email: {user.email} with username: {user.username} already registered"
        )
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/api/users", response_model=list[UserResponse])
def get_users(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 10
):
    users = db.execute(
        select(models.User)
        .order_by(models.User.username.asc())
        .offset(skip)
        .limit(limit)
    ).scalars().all()

    return users

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    
    user = db.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return user

## get user post
@app.get("/api/users/{user_id}/posts", response_model=List[PostResponse])
def get_user_posts(user_id: int, db : Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return posts

@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,       # how many to skip (for pagination)
    limit: int = 10      # how many to return
):
    posts = db.execute(
        select(models.Post)
        .order_by(models.Post.date_posted.desc())  # newest first
        .offset(skip)
        .limit(limit)
    ).scalars().all()

    return posts

@app.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    
    # check if user exists
    user = db.execute(
        select(models.User).where(models.User.id == post.user_id)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):

    post = db.execute(
        select(models.Post).where(models.Post.id == post_id)
    ).scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    return post

@app.patch(
    "/api/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    # Get user
    result = db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    # Check username uniqueness
    if user_update.username and user_update.username != user.username:
        result = db.execute(
            select(models.User).where(
                models.User.username == user_update.username
            )
        )
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
    # Check email uniqueness
    if user_update.email and user_update.email != user.email:
        result = db.execute(
            select(models.User).where(
                models.User.email == user_update.email
            )
        )
        existing_email = result.scalars().first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
    # Dynamic update
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@app.delete(
    "/api/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db.delete(user)
    db.commit()
    return None

@app.put("/api/posts/{post_id}", response_model=PostResponse)
def update_post_full(
    post_id: int,
    post_data: PostCreate,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if post_data.user_id != post.user_id:
        result = db.execute(
            select(models.User).where(models.User.id == post_data.user_id),
        )
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id

    db.commit()
    db.refresh(post)
    return post


@app.patch("/api/posts/{post_id}", response_model=PostResponse)
def update_post_partial(
    post_id: int,
    post_data: PostUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    db.delete(post)
    db.commit()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    message = exc.detail if exc.detail else "An error occurred."
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exc.status_code,       
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": exc.status_code,     
            "title": exc.status_code,
            "message": message
        },
        status_code=exc.status_code          
    )

## Adding validation error handler to return JSON responses for API routes
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )
    # For non-API routes, you can choose to render an error page or return a generic response
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": "Validation Error",
            "message": "Invalid input data. Please check your request and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )