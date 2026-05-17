from pydoc_data.topics import topics

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from httpx import request

app = FastAPI()

# This line is what you're missing
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "title": "Why I Love FastAPI",
        "excerpt": "FastAPI has completely changed how I build APIs. The automatic documentation, type hints, and async support make development so much faster.",
        "author": {
            "username": "CoreyMSchafer",
            "initials": "CM",
            "avatar_color": "#1a2d45",
        },
        "tags": ["FastAPI", "Backend"],
        "likes_count": 142,
        "comments_count": 18,
        "read_time": 5,
        "created_at": "December 31, 2025",
        "is_liked": False,
    },
    {
        "id": 2,
        "title": "Async/Await Finally Clicked",
        "excerpt": "I've been struggling with async programming for months, but FastAPI's approach finally made it click for me.",
        "author": {
            "username": "PoppyTheCoder",
            "initials": "PT",
            "avatar_color": "#0e3040",
        },
        "tags": ["Async", "Python", "Beginner"],
        "likes_count": 213,
        "comments_count": 34,
        "read_time": 7,
        "created_at": "December 27, 2025",
        "is_liked": True,
    },
    {
        "id": 3,
        "title": "SQLAlchemy 2.0 — What You Need to Know",
        "excerpt": "The new SQLAlchemy 2.0 API with FastAPI is a game changer. The mapped_column syntax is much more intuitive.",
        "author": {
            "username": "FarmDogs",
            "initials": "FD",
            "avatar_color": "#1a3820",
        },
        "tags": ["SQLAlchemy", "Database"],
        "likes_count": 58,
        "comments_count": 7,
        "read_time": 4,
        "created_at": "December 26, 2025",
        "is_liked": False,
    },
    # ── 3 new posts below ──────────────────────────────────────
    {
        "id": 4,
        "title": "JWT Authentication From Scratch",
        "excerpt": "Tokens, expiry, refresh flows — JWT auth sounds scary until you break it down. Here's how I implemented it cleanly in FastAPI with zero third-party auth libraries.",
        "author": {
            "username": "ZaraR_codes",
            "initials": "ZR",
            "avatar_color": "#3a1010",
        },
        "tags": ["JWT", "Auth", "Security"],
        "likes_count": 176,
        "comments_count": 22,
        "read_time": 6,
        "created_at": "December 25, 2025",
        "is_liked": False,
    },
    {
        "id": 5,
        "title": "Docker + FastAPI: The Setup I Use on Every Project",
        "excerpt": "A Dockerfile, a compose file, a .env — that's all you need. I've refined this setup across a dozen projects and it handles dev, staging, and prod without changing a line.",
        "author": {
            "username": "TheLukeDev",
            "initials": "TL",
            "avatar_color": "#0e2d3a",
        },
        "tags": ["Docker", "DevOps", "FastAPI"],
        "likes_count": 94,
        "comments_count": 11,
        "read_time": 5,
        "created_at": "December 24, 2025",
        "is_liked": True,
    },
    {
        "id": 6,
        "title": "Stop Writing Spaghetti Routes — Use APIRouter",
        "excerpt": "When your main.py hits 400 lines you know something went wrong. APIRouter lets you split your FastAPI app into clean, modular files the way it was always meant to be.",
        "author": {
            "username": "NinaK_writes",
            "initials": "NK",
            "avatar_color": "#2d1a40",
        },
        "tags": ["FastAPI", "Clean Code", "Backend"],
        "likes_count": 311,
        "comments_count": 45,
        "read_time": 8,
        "created_at": "December 23, 2025",
        "is_liked": False,
    },
]


@app.get("/")
def home(request: Request):
    recent_posts = [
        {"emoji": "📡", "title": "Building Real-Time APIs with WebSockets", "author": "PoppyTheCoder", "time_ago": "2h ago"},
        {"emoji": "🔐", "title": "JWT Auth Patterns in FastAPI",            "author": "CoreyMSchafer", "time_ago": "5h ago"},
        {"emoji": "🐘", "title": "PostgreSQL vs SQLite for Development",    "author": "FarmDogs",      "time_ago": "1d ago"},
        {"emoji": "🎨", "title": "CSS Grid Layout Deep Dive",               "author": "GoodBoyBronx", "time_ago": "2d ago"},
    ]

    suggested_writers = [
        {"initials": "NK", "username": "NinaK_writes", "bio": "Systems design & distributed…"},
        {"initials": "TL", "username": "TheLukeDev",   "bio": "React, TypeScript, Tailwind…"},
        {"initials": "MH", "username": "MHasan_io",    "bio": "ML engineer, open source…"},
        {"initials": "ZR", "username": "ZaraR_codes",  "bio": "DevOps, Kubernetes, AWS…"},
    ]

    topics = [
        {"name": "Latest Posts",   "post_count": 128},
        {"name": "Announcements",  "post_count": 14},
        {"name": "Python & FastAPI","post_count": 87},
        {"name": "Frontend Dev",   "post_count": 56},
        {"name": "Databases",      "post_count": 43},
        {"name": "Misc & etc",     "post_count": 22},
    ]
# NEW style — request is a separate argument
    return templates.TemplateResponse(
        name="home.html",
        request=request,
        context={
            "active_page": "home",
            "posts": posts,
            "recent_posts": recent_posts,
            "suggested_writers": suggested_writers,
            "topics": topics,
        }
    )

@app.get("/profile")
def profile(request: Request):

    # ── Fake user object ───────────────────────────────
    class FakeUser:
        full_name      = "Amara Osei"
        username       = "amara_osei"
        email          = "amara@inkwell.com"
        bio            = "Backend engineer & technical writer. I build with FastAPI, Python, and PostgreSQL."
        location       = "Lagos, Nigeria"
        avatar_url     = None
        initials       = "AO"
        posts_count    = 6
        followers_count = 284
        following_count = 91
        liked_count    = 47
        joined_at      = "January 2025"
        tags           = ["FastAPI", "Python", "Backend"]

        posts = [
            {
                "id": 1,
                "title": "Why I Love FastAPI",
                "excerpt": "FastAPI has completely changed how I build APIs. The automatic documentation, type hints, and async support make development so much faster.",
                "tags": ["FastAPI", "Backend"],
                "likes_count": 142,
                "comments_count": 18,
                "created_at": "Dec 31, 2025",
                "read_time": 5,
            },
            {
                "id": 2,
                "title": "JWT Authentication From Scratch",
                "excerpt": "Tokens, expiry, refresh flows — JWT auth sounds scary until you break it down. Here's how I implemented it cleanly in FastAPI.",
                "tags": ["Auth", "JWT", "Security"],
                "likes_count": 176,
                "comments_count": 22,
                "created_at": "Dec 25, 2025",
                "read_time": 6,
            },
            {
                "id": 3,
                "title": "SQLAlchemy 2.0 — What You Need to Know",
                "excerpt": "The new SQLAlchemy 2.0 API with FastAPI is a game changer. The mapped_column syntax is much more intuitive.",
                "tags": ["SQLAlchemy", "Database"],
                "likes_count": 58,
                "comments_count": 7,
                "created_at": "Dec 26, 2025",
                "read_time": 4,
            },
            {
                "id": 4,
                "title": "Stop Writing Spaghetti Routes — Use APIRouter",
                "excerpt": "When your main.py hits 400 lines you know something went wrong. APIRouter lets you split your FastAPI app into clean, modular files.",
                "tags": ["FastAPI", "Clean Code"],
                "likes_count": 311,
                "comments_count": 45,
                "created_at": "Dec 23, 2025",
                "read_time": 8,
            },
        ]

        followers = [
            {"initials": "NK", "username": "NinaK_writes",  "bio_short": "Systems design & distributed…"},
            {"initials": "TL", "username": "TheLukeDev",    "bio_short": "React, TypeScript, Tailwind…"},
            {"initials": "MH", "username": "MHasan_io",     "bio_short": "ML engineer, open source…"},
            {"initials": "ZR", "username": "ZaraR_codes",   "bio_short": "DevOps, Kubernetes, AWS…"},
        ]

        following = [
            {"initials": "CM", "username": "CoreyMSchafer", "bio_short": "FastAPI, Python, Backend…"},
            {"initials": "NK", "username": "NinaK_writes",  "bio_short": "Systems design & distributed…"},
            {"initials": "FD", "username": "FarmDogs",      "bio_short": "SQLAlchemy, databases…"},
        ]

        liked_posts = [
            {
                "id": 1,
                "title": "Why I Love FastAPI",
                "excerpt": "FastAPI has completely changed how I build APIs.",
                "author": {"username": "CoreyMSchafer"},
            },
            {
                "id": 3,
                "title": "Async/Await Finally Clicked",
                "excerpt": "I've been struggling with async programming for months, but FastAPI's approach finally made it click.",
                "author": {"username": "PoppyTheCoder"},
            },
        ]

        top_post = {
            "id": 4,
            "title": "Stop Writing Spaghetti Routes — Use APIRouter",
            "likes_count": 311,
            "comments_count": 45,
            "created_at": "Dec 23, 2025",
            "read_time": 8,
        }

    return templates.TemplateResponse(name="profile.html", 
        request=request,
        context= {
            "active_page": "writers",
            "user": FakeUser(),
       }
    )
