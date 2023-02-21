from fastapi import APIRouter, Depends, status, HTTPException, status
from jose import jwt
import schemas, JWTtoken, database, models
from fastapi.security import OAuth2PasswordRequestForm
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentcate']
)


@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user available")

    if not check_password_hash(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credential")

    access_token = JWTtoken.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}