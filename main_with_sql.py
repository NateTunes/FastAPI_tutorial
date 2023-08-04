
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host='127.0.0.1',
                                database='fastapi',
                                user='postgres',
                                password='pass123',
                                cursor_factory=RealDictCursor
                                )
        cursor = conn.cursor()
        print("Successful connection")
        break
    except Exception as ex:
        time.sleep(1)
        print("Exception while connecting", ex)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    res = cursor.fetchall()
    return {"data": res}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    res = cursor.fetchone()
    conn.commit()
    return {"data": res}


@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE ID = %s""", (str(id)))
    post = cursor.fetchall()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post of id = {id}")

    return {"data": post}


@app.delete("/posts/{id}")
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post of id = {id}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    new_post = cursor.fetchone()
    conn.commit()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find post of id = {id}")
    return {"data": new_post}