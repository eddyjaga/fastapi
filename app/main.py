from socketserver import ThreadingUnixDatagramServer
from time import sleep
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row

from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# while True:
#     try:
#         conn = psycopg.connect(
#             "dbname=db_fastapi user=amgaa", row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("error: ", error)
#         sleep(2)


@app.get("/")
async def root():
    return {"message": "Welcome to Fast API"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
async def get_post(id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.post_id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The page not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Posts).filter(
        models.Posts.post_id == id).delete(synchronize_session=False)
    db.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    return {"message": "Post was successfully deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    updated_post_query = db.query(models.Posts).filter(
        models.Posts.post_id == id)

    updated_post = updated_post_query.first()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": updated_post_query.first()}
