from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    path = Column(String)
    types = Column(String, default='Image')
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates="media")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post", uselist=False)
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
