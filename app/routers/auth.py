from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import database
from app import schemas
from app import models
from app import utils
from app import oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create and return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}