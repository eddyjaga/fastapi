from socketserver import ThreadingUnixDatagramServer
from time import sleep
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row

app = FastAPI()
while True:
    try:
        conn = psycopg.connect(
            "dbname=db_fastapi user=amgaa", row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("error: ", error)
        sleep(2)


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "Welcome to Fast API"}


@app.get("/posts")
async def get_posts():
    posts = cursor.execute("SELECT * FROM posts").fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (post_title, post_content, published) 
        VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.get("/posts/{id}")
async def get_post(id: int):
    post = cursor.execute(
        """ SELECT * FROM posts WHERE post_id = %s """, [id]).fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The page not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    deleted_post = cursor.execute(
        """DELETE FROM posts WHERE post_id =%s RETURNING *""", [id]).fetchone()

    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    return {"message": "Post was successfully deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    updated_post = cursor.execute("""UPDATE posts SET post_title = %s, post_content = %s, published = %s WHERE post_id = %s RETURNING *""", [
                                  post.title, post.content, post.published, id]).fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"data": updated_post}
