from fastapi import FastAPI
from .routers import post, user, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
