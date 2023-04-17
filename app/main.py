from fastapi import FastAPI, UploadFile, File, Depends
from app.database import engine, Base
from app import models, database, schemas, authentication
from app.routers import file_router, comment_router, post_router, user_router
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

app = FastAPI()


app.include_router(authentication.router)
app.include_router(file_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
app.include_router(user_router.router)


@app.get('/', tags=['Home'])
async def home():
    return {'message':'Welcome to Social APIs'}