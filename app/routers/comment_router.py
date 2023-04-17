from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app import models, database, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    tags=['Comments'],
    prefix='/comment'
)

@router.post("/")
async def create_comment(comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user:schemas.Comment=Depends(get_current_user)):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get('/')
async def all_comment(db:Session=Depends(database.get_db), current_user:schemas.Comment=Depends(get_current_user)):
    comments = db.query(models.Comment).all()
    return comments

@router.get("/{id}", response_model=schemas.Comment)
async def read_comment(id: int, db: Session = Depends(database.get_db), current_user:schemas.Comment=Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No comment available with this id {id}")
    return comment

@router.put("/{id}")
async def update_comment(id: int, comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user:schemas.Comment=Depends(get_current_user)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No comment available with this id {id}")
    update_data = comment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment 

@router.delete("/{id}")
async def delete_comment(id, db: Session = Depends(database.get_db), current_user:schemas.Comment=Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No comment available with this id {id}")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}
