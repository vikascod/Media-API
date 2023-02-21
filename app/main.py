from fastapi import FastAPI, UploadFile, File, Depends
from database import engine, Base
import models, database, schemas, file_router, comment_router, post_router, user_router, authentication
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

app = FastAPI()


app.include_router(authentication.router)
app.include_router(file_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
app.include_router(user_router.router)