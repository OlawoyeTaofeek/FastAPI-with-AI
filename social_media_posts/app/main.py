from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel, Field
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
from typing import List  

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime


class PostsResponse(BaseModel):
    data: List[PostResponse]
    

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="fastapi",
            user="postgres",
            password="oladipupo",
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()

        print("Database Connection was successful")
        break

    except (psycopg2.DatabaseError, Exception) as e:
        print("Connecting to database failed")
        print(f"Error: {e}")
        time.sleep(5)

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/posts", response_model=PostsResponse, description="Returns all blog posts from database")
async def get_posts():

    cursor.execute("""SELECT * FROM "Posts" """)

    posts = cursor.fetchall()

    return {"data": posts}

@app.post("/posts")
async def create_post(post: Post):
    cursor.execute(
        """
        INSERT INTO "Posts" (title, content, published)
        VALUES (%s, %s, %s)
        RETURNING *
        """,
        (post.title, post.content, post.published)
    )

    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM "Posts" WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# 204 No Content means: Requests Succeeded, server returns No response body
async def delete_post(id: int):
    cursor.execute("""Delete FROM "Posts" WHERE id = %s RETURNING * """, (str(id),)) 
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE "Posts" SET title = %s, content = %s, published = %s WHERE id = %sRETURNING *""", 
                   (post.title, post.content, post.published, (str(id)), ))
    
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
    return {"data": updated_post}