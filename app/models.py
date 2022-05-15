from enum import unique
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from .database import Base


class Posts(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, nullable=False)
    post_title = Column(String, nullable=False)
    post_content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
