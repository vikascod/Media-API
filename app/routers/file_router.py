from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from database import engine, Base
import models, database, schemas
from sqlalchemy.orm import Session
import uuid
import os
from oauth2 import get_current_user

router = APIRouter(
    tags=['Files']
)


@router.post("/file")
async def create_file(file: UploadFile, db:Session=Depends(database.get_db), current_user:schemas.Media=Depends(get_current_user)):
    file_id = str(uuid.uuid4())
    filename = file.filename
    file_path = os.path.join('Media_Folder', file.filename)
    post_id = 1
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    new_file = models.Media(filename=filename, path=file_path, post_id=post_id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


@router.get('/file')
async def all_media(db:Session=Depends(database.get_db), current_user:schemas.Media=Depends(get_current_user)):
    files = db.query(models.Media).all()
    return files

@router.get("/file/{file_id}", response_model=schemas.Media)
async def read_file(file_id: int, db:Session=Depends(database.get_db), current_user:schemas.Media=Depends(get_current_user)):
    file = db.query(models.Media).get(file_id)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media')
    return file

@router.put("/file/{file_id}")
async def update_file(file_id: int, file: UploadFile, db:Session=Depends(database.get_db), current_user:schemas.Media=Depends(get_current_user)):
    file_to_update = db.query(models.Media).get(file_id)
    if not file_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No any media')
    filename = file.filename
    # if not os.path.exists("media"):
    #     os.makedirs("media")
    # MEDIA_FOLDER = os.path.abspath("media")
    file_path = os.path.join('Media_Folder', file.filename)
    post_id = 1
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    file_to_update.filename = filename
    file_to_update.path = file_path
    file_to_update.post_id = post_id
    db.commit()
    db.refresh(file_to_update)
    return file_to_update


@router.delete("/file/{file_id}")
async def delete_file(file_id: int, db:Session=Depends(database.get_db), current_user:schemas.Media=Depends(get_current_user)):
    file = db.query(models.Media).get(file_id)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No media')
    db.delete(file)
    db.commit()
    return {"message": "File deleted"}
