from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException # To return HTML responses
from fastapi.exceptions import RequestValidationError # To handle validation errors
from fastapi.responses import JSONResponse # To return JSON responses for errors
from .schema import PostCreate, PostResponse
from typing import List
from datetime import timezone, datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = "home.html",
        context={"posts": posts, "title": "Home"},
    )

@app.get("/posts/{id}", include_in_schema=False, name="post")
def get_post(id: int, request: Request):
    for post in posts:
        if post.get("id") == id:
            return templates.TemplateResponse(
                request=request,
                name = "post.html",
                context={"post": post, "title": post.get("title")[:50]},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts", response_model=List[PostResponse])
def get_posts():
    return posts

@app.post(
    "/api/posts_create",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
def create_post(post: PostCreate):

    new_post = post.model_dump()

    new_post["id"] = max([p["id"] for p in posts], default=0) + 1

    new_post["date_posted"] = datetime.now(timezone.utc)

    posts.append(new_post)

    return new_post


@app.get("/api/posts/{id}", response_model=PostResponse)
def get_post_(id: int):
    for post in posts:
        if post.get("id") == id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

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