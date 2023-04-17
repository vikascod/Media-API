import os
import uuid
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from app.database import engine, Base
from app import models, database, schemas
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user
from typing import List, Optional

router = APIRouter(
    tags=['Posts']
)


@router.post("/post")
async def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user:schemas.Post=Depends(get_current_user)):
    db_post = models.Post(author_id=current_user.id, **post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get('/post', response_model=List[schemas.Post])
async def all_post(db:Session=Depends(database.get_db), current_user:schemas.PostCreate=Depends(get_current_user), limit:int=5, skip:int=0, search:Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    return posts


@router.get("/post/{id}", response_model=schemas.Post)
async def read_post(id: int, db: Session = Depends(database.get_db), current_user:schemas.PostCreate=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post available")
    return post

@router.put("/post/{post_id}")
async def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user:schemas.Post=Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post available")
    # if db_post.author_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized action")
    update_data = post.dict(exclude_unset=True)
    db.query(models.Post).filter(models.Post.id == post_id).update(update_data)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/post/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(database.get_db), current_user:schemas.Post=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post available")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
