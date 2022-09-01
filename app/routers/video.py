from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import oauth2, models, schemas
from app.database import get_db

router = APIRouter()


@router.get("/videos")
def get_all_videos(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    videos = db.query(models.Video).filter(models.Video.user_id == current_user.id).all()
    return {"data": videos}


@router.post("/videos", response_model=schemas.VideoResponse)
def upload_new_video(video: schemas.VideoBase, db: Session = Depends(get_db),
                     current_user: models.User = Depends(oauth2.get_current_user)):
    new_video = models.Video(user_id=current_user.id, **video.dict())
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return new_video
