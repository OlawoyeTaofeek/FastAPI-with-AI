from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi import HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import models
from .async_database import Base, engine, get_db
from .schema import (
    PostCreate,
    PostResponse,
    PostUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from .utils import format_date


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Create DB tables on startup and dispose the engine on shutdown."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")
templates.env.filters["format_date"] = format_date

# Convenience type alias used throughout
DB = Annotated[AsyncSession, Depends(get_db)]


# ---------------------------------------------------------------------------
# HTML / template routes
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
async def home(request: Request, db: DB):
    """Display all posts in descending date order."""
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .order_by(models.Post.date_posted.desc())
    )
    posts = result.scalars().all()

    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts},
    )


@app.get("/posts/{post_id}", include_in_schema=False, name="post")
async def post_page(request: Request, post_id: int, db: DB):
    """Display a specific post by ID."""
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return templates.TemplateResponse(
        request,
        "post.html",
        {"post": post, "title": post.title[:50]},
    )


@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
async def user_posts_page(request: Request, user_id: int, db: DB):
    """Display all posts written by a specific user."""
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id)
    )
    posts = result.scalars().all()

    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )


# ---------------------------------------------------------------------------
# User API endpoints
# ---------------------------------------------------------------------------

@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserCreate, db: DB):
    """Create a new user after checking for duplicate email / username."""
    result = await db.execute(
        select(models.User).where(
            or_(
                models.User.email == user.email,
                models.User.username == user.username,
            )
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"A user with email '{user.email}' or "
                f"username '{user.username}' already exists."
            ),
        )

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.get("/api/users", response_model=list[UserResponse])
async def get_users(db: DB, skip: int = 0, limit: int = 10):
    """Retrieve all users, ordered by username, with pagination."""
    result = await db.execute(
        select(models.User)
        .order_by(models.User.username.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DB):
    """Retrieve a single user by ID."""
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )

    return user


@app.patch("/api/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: DB):
    """Partially update a user; validates uniqueness of email / username."""
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Username uniqueness check
    if user_update.username and user_update.username != user.username:
        result = await db.execute(
            select(models.User).where(
                models.User.username == user_update.username
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken.",
            )

    # Email uniqueness check
    if user_update.email and user_update.email != user.email:
        result = await db.execute(
            select(models.User).where(
                models.User.email == user_update.email
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: DB):
    """Delete a user by ID."""
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    await db.delete(user)
    await db.commit()
    return None


# ---------------------------------------------------------------------------
# Post API endpoints
# ---------------------------------------------------------------------------

@app.get("/api/posts", response_model=list[PostResponse])
async def get_posts(db: DB, skip: int = 0, limit: int = 10):
    """Retrieve all posts in descending date order with pagination."""
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .order_by(models.Post.date_posted.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(post: PostCreate, db: DB):
    """Create a new post, verifying that the author exists."""
    result = await db.execute(
        select(models.User).where(models.User.id == post.user_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )
    db.add(new_post)
    await db.commit()
    # Eagerly load the author relationship before returning
    await db.refresh(new_post, attribute_names=["author"])
    return new_post


@app.get("/api/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: DB):
    """Retrieve a single post by ID."""
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found.",
        )

    return post


@app.put("/api/posts/{post_id}", response_model=PostResponse)
async def update_post_full(post_id: int, post_data: PostCreate, db: DB):
    """Fully replace a post's fields."""
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found.",
        )

    # Validate the new owner only when user_id changes
    if post_data.user_id != post.user_id:
        result = await db.execute(
            select(models.User).where(models.User.id == post_data.user_id)
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id

    await db.commit()
    await db.refresh(post, attribute_names=["author"])
    return post


@app.patch("/api/posts/{post_id}", response_model=PostResponse)
async def update_post_partial(post_id: int, post_data: PostUpdate, db: DB):
    """Partially update a post's fields."""
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found.",
        )

    for field, value in post_data.model_dump(exclude_unset=True).items():
        setattr(post, field, value)

    await db.commit()
    # Reload with author so the response model is fully populated
    await db.refresh(post, attribute_names=["author"])
    return post


@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: DB):
    """Delete a post by ID."""
    result = await db.execute(
        select(models.Post).where(models.Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found.",
        )

    await db.delete(post)
    await db.commit()
    return None  


@app.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
async def get_user_posts(user_id: int, db: DB):
    """Retrieve all posts written by a specific user."""
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )

    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id)
    )
    return result.scalars().all()


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException,
):
    """Return JSON for /api routes; render an error page for everything else."""
    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": exception.detail or "An unexpected error occurred.",
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    """Return JSON for /api routes; render an error page for everything else."""
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception)

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )