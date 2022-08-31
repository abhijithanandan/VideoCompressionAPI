from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import oauth2, models
from app.database import get_db

router = APIRouter()


@router.get("/videos/{id}")
def get_all_videos(id: int, db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    videos = db.query(models.Video).filter(models.Video.user_id == user_id).all()
    return {"data": videos}
