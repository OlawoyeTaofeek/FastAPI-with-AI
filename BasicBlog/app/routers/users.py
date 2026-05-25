"""
User Router
-----------
Handles all user-related endpoints:
  - Registration & authentication (JWT via OAuth2 Bearer)
  - Profile retrieval & updates
  - User deletion
  - Fetching posts belonging to a user

Base prefix : /api/users
Tags        : Users
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import timedelta

from ..async_database import get_db
from .. import models
from ..schema import UserCreate, UserResponse, UserUpdate, PostResponse, Token, TokenData
from ..auth import create_access_token, verify_access_token
from ..config import settings
from ..utils import hash_password, verify_password


# ---------------------------------------------------------------------------
# Router & shared dependencies
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/api/users", tags=["Users"])

# Tells FastAPI where the token endpoint lives so Swagger UI can show
# the Authorize 🔒 button and send Bearer tokens automatically.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

# Reusable DB session dependency — injected into every route that needs it.
DB = Annotated[AsyncSession, Depends(get_db)]


# ---------------------------------------------------------------------------
# Helper dependency — resolves the current authenticated user from a JWT.
# Used as a Depends() in any protected route instead of duplicating logic.
# ---------------------------------------------------------------------------

async def get_authenticated_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> models.User:
    """
    Decode the Bearer JWT and return the matching User row.

    Raises 401 if the token is invalid, expired, or the user no longer exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Decode JWT → TokenData(username=email)
    token_data: TokenData = verify_access_token(
        token, credentials_exception=credentials_exception
    )

    result = await db.execute(
        select(models.User).where(
            func.lower(models.User.email) == token_data.username.lower()
        )
    )
    user = result.scalar_one_or_none()
    if not user:
        raise credentials_exception
    return user


# ---------------------------------------------------------------------------
# Auth endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/token",
    response_model=Token,
    summary="Login — obtain a JWT access token",
    responses={
        200: {"description": "Login successful, JWT returned."},
        401: {"description": "Invalid email or password."},
    },
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Authenticate a user and return a signed JWT access token.

    - **username** field in the form is treated as the user's **email** or **username**.
    - Password is verified against the stored bcrypt hash.
    - Token expiry is controlled by `ACCESS_TOKEN_EXPIRE_MINUTES` in settings.
    """
    # Look up user by email (case-insensitive)
    login_input = form_data.username.lower().strip()

    # Try to find the user by email first, then fall back to username
    result = await db.execute(
        select(models.User).where(
            or_(
                func.lower(models.User.email)    == login_input,
                func.lower(models.User.username) == login_input,
            )
        )
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email},  # always store email in the token — it's unique
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return Token(access_token=access_token, token_type="bearer")


# ---------------------------------------------------------------------------
# Current-user endpoint (protected)
# ---------------------------------------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get the currently authenticated user",
    responses={
        200: {"description": "Authenticated user profile."},
        401: {"description": "Missing, invalid, or expired token."},
    },
)
async def get_current_user(
    current_user: Annotated[models.User, Depends(get_authenticated_user)],
):
    """
    Return the profile of the user who owns the Bearer token.

    Requires a valid JWT in the `Authorization: Bearer <token>` header.
    """
    return current_user


# ---------------------------------------------------------------------------
# CRUD endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        201: {"description": "User created successfully."},
        400: {"description": "Email or username already in use."},
    },
)
async def create_user(user: UserCreate, db: DB):
    """
    Register a new user account.

    - Checks for duplicate **email** and **username** in a single query.
    - Normalises email and username to lowercase before saving.
    - Password is hashed with bcrypt before being stored — never saved as plain text.
    """
    # Single query to catch either duplicate email or duplicate username
    result = await db.execute(
        select(models.User).where(
            or_(
                func.lower(models.User.email)    == user.email.lower(),
                func.lower(models.User.username) == user.username.lower(),
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

    # Normalise & hash before persisting
    user.email    = user.email.lower()
    user.username = user.username.lower()
    user.password = hash_password(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # reload to get DB-generated fields (id, created_at, etc.)
    return new_user


@router.get(
    "",
    response_model=list[UserResponse],
    summary="List all users (paginated)",
    responses={
        200: {"description": "Paginated list of users ordered by username."},
    },
)
async def get_users(db: DB, skip: int = 0, limit: int = 10):
    """
    Retrieve a paginated list of all users, sorted alphabetically by username.

    - **skip**: number of records to skip (offset). Default `0`.
    - **limit**: maximum records to return. Default `10`, keep reasonable to avoid large payloads.
    """
    result = await db.execute(
        select(models.User)
        .order_by(models.User.username.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get a single user by ID",
    responses={
        200: {"description": "User found."},
        404: {"description": "No user with that ID exists."},
    },
)
async def get_user(user_id: int, db: DB):
    """
    Retrieve a single user's profile by their numeric **user_id**.
    """
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


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Partially update a user",
    responses={
        200: {"description": "User updated successfully."},
        400: {"description": "New email or username is already taken."},
        404: {"description": "User not found."},
    },
)
async def update_user(user_id: int, user_update: UserUpdate, db: DB):
    """
    Partially update a user's profile (PATCH semantics — only send fields to change).

    - **email** changes are checked for uniqueness before being applied.
    - **username** changes are checked for uniqueness before being applied.
    - Email is stored lowercase; other fields are saved as-is.
    """
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Only check uniqueness if the username is actually changing
    if user_update.username and user_update.username.lower() != user.username.lower():
        result = await db.execute(
            select(models.User).where(
                func.lower(models.User.username) == user_update.username.lower()
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken.",
            )

    # Only check uniqueness if the email is actually changing
    if user_update.email and user_update.email.lower() != user.email.lower():
        result = await db.execute(
            select(models.User).where(
                func.lower(models.User.email) == user_update.email.lower()
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

    # Apply only the fields that were explicitly provided (exclude_unset=True)
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value.lower() if key == "email" else value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    responses={
        204: {"description": "User deleted. No content returned."},
        404: {"description": "User not found."},
    },
)
async def delete_user(user_id: int, db: DB):
    """
    Permanently delete a user by their numeric **user_id**.

    Returns `204 No Content` on success — no response body.
    """
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
# Relational endpoint — user's posts
# ---------------------------------------------------------------------------

@router.get(
    "/{user_id}/posts",
    response_model=list[PostResponse],
    summary="Get all posts by a specific user",
    responses={
        200: {"description": "List of posts authored by the user, newest first."},
        404: {"description": "User not found."},
    },
)
async def get_user_posts(user_id: int, db: DB):
    """
    Retrieve all posts written by the user identified by **user_id**.

    - Posts are ordered by `date_posted` descending (newest first).
    - The post author relationship is eagerly loaded via `selectinload`
      to avoid N+1 query issues when serialising `PostResponse`.
    """
    # Verify the user exists before querying posts
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )

    # Eagerly load the author relationship to prevent N+1 queries
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id)
        .order_by(models.Post.date_posted.desc())
    )
    return result.scalars().all()