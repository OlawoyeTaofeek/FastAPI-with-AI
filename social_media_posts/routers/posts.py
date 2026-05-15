from fastapi import status, Response, HTTPException, Depends, APIRouter
from app import models  
from typing import List, Optional
from app.database import get_db
from sqlalchemy.orm import Session
from app.schema import PostCreate, PostResponse, PostWithCommentsOut, PostsResponse, PostResponseLike
from oauth2 import get_current_user
from app.models import User
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import joinedload
# from app.utils import generate_embedding

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/posts_with_comments", status_code=status.HTTP_200_OK, response_model=list[PostWithCommentsOut])
def get_all_posts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)  # 👈 make sure token is sent
):
    posts = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.comments),
            joinedload(models.Post.likes),
        )
        .all()
    )

    return [
        PostWithCommentsOut(**{
            "id": post.id,
            "title": post.title,
            "likes": len(post.likes),
            "comments": [{"id": c.id, "content": c.content} for c in post.comments],
        })
        for post in posts
    ]

@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db), user: User = Depends(get_current_user), limit: int = 5, skip: int = 0):
    posts = db.query(models.Post).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts available")
    print(posts)
    return posts

@router.get("/post_with_likes", response_model=List[PostResponseLike])
def get_posts(
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user),
    limit: int = 3,
    skip: int = 0     
):
    posts = (
        db.query(models.Post, func.count(models.Like.post_id).label("likes"))
        .outerjoin(models.Like, models.Like.post_id == models.Post.id)
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available")

    result = [
        PostResponseLike.model_validate({   
            **post.__dict__, 
            "likes": count, 
            "owner": db.query(models.User).filter(models.User.id == post.user_id).first()
        })
        for post, count in posts
    ]
    return result


## Get post with search: keyword search, full text search, and semantic search
@router.get("/keyword_search", response_model=List[PostResponse])
def get_posts_by_keyword_search(db: Session = Depends(get_db), 
            user: User = Depends(get_current_user), 
            limit: int = 5, 
            skip: int = 0,
            search: Optional[str] = None
        ):
    
    query = db.query(models.Post)
    if search:
        query = query.filter(
            or_(
                models.Post.title.ilike(f"%{search}%"),
                models.Post.content.ilike(f"%{search}%")
            )
        )
    posts = query.limit(limit).offset(skip).all()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts available")
    return posts

# @router.get("/semantic_search", response_model=List[PostResponse])
# def semantic_search(q: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     # generate embedding for the search query
#     query_embedding = generate_embedding(q)

#     posts = db.query(models.Post)\
#               .filter(models.Post.embedding.isnot(None))\
#               .order_by(models.Post.embedding.cosine_distance(query_embedding))\
#               .limit(5)\
#               .all()

#     if not posts:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matching posts found")

#     return posts

@router.get("/user_post", response_model=PostsResponse)
def get_posts_by_user(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == user.id).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return {"data": posts}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # print("Authenticated user:", user.id, user.email)  
    # print("Post data:", post.model_dump())              
    
    new_posts = models.Post(**post.model_dump(), user_id=user.id)
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
# def create_posts(post: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     # generate embedding from title + content
#     embedding = generate_embedding(f"{post.title} {post.content}")

#     new_posts = models.Post(
#         **post.model_dump(),
#         user_id=user.id,
#         embedding=embedding  # 👈 attach the embedding
#     )
#     db.add(new_posts)
#     db.commit()
#     db.refresh(new_posts)
#     return new_posts

@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    post = db.query(models.Post)\
             .filter(models.Post.id == id)\
             .first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
    return post

@router.get("/get_post_with_likes/{id}", response_model=PostResponseLike)
def get_post_with_likes(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    post = db.query(models.Post)\
             .filter(models.Post.id == id)\
             .outerjoin(models.Like, models.Like.post_id == models.Post.id)\
             .group_by(models.Post.id)\
             .add_columns(func.count(models.Like.post_id).label("likes")).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
    return PostResponseLike.model_validate({
        **post.Post.__dict__,
        "likes": post.likes,
        "owner": db.query(models.User).filter(models.User.id == post.Post.user_id).first()
    })


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id, models.Post.user_id == user.id)
    
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: PostCreate, db:Session = Depends(get_db), user: User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(
        and_(
               models.Post.id == id,
               models.Post.user_id == user.id
            )
        )
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post wth id: {id} was not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()
