from pydantic import BaseModel


class Post(BaseModel):
    post_title: str
    post_content: str
    published: bool = True
