from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, database
import uuid
from werkzeug.security import generate_password_hash
from app.oauth2 import get_current_user

router = APIRouter(
    tags=['Users']
)

@router.post('/')
async def register(user:schemas.UserCreate, db:Session=Depends(database.get_db)):
    new_user = models.User(username=user.username, email=user.email, password=generate_password_hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.User)
async def show(id, db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user available")

    return user


@router.put('/{id}')
async def update(id, user:schemas.User, db:Session=Depends(database.get_db), current_user:schemas.User=Depends(get_current_user)):
    user_update = db.query(models.User).filter(models.User.id==id).first()
    if not user_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user available")
    user_update.username = user.username
    user_update.email = user.email
    user_update.password = generate_password_hash(user.password)
    db.commit()
    db.refresh(user_update)
    return user_update


@router.delete('/{id}')
async def destroy(id, db:Session=Depends(database.get_db), current_user:schemas.User=Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user available with id {id}")
    db.delete(user)
    db.commit()
    return "Post Deleted"