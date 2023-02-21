from pydantic import BaseModel
from datetime import datetime
from typing import Union
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class User(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True

class MediaBase(BaseModel):
    filename : str
    path: str
    types : str

class MediaCreate(MediaBase):
    pass

class Media(BaseModel):
    filename : str
    path: str
    types : str
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    body: str

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    id: int
    title: str
    body: str
    # author: User
    # media: Media
    author: Optional[User] = None
    media: Optional[Media] = None
    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    body: str
    author_id: int
    post_id: int

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    author: User
    post: Post
    class Config:
        orm_mode = True
